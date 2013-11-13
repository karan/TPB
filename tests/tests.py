from datetime import datetime, timedelta
import itertools
import sys
import os
import unittest

from bs4 import BeautifulSoup

from tpb.tpb import TPB, Search, Recent, Top, List, Paginated
from tpb.constants import ConstantType, Constants, ORDERS, CATEGORIES
from tpb.utils import URL

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from tests.cases import RemoteTestCase
    unicode = str
else:
    from urllib2 import urlopen
    from cases import RemoteTestCase


class ConstantsTestCase(RemoteTestCase):
    def test_extension(self):
        checks = [ORDERS, CATEGORIES]
        while checks:
            current = checks.pop()
            for name, attr in current.__dict__.items():
                if isinstance(attr, type):
                    self.assertTrue(attr.__class__, ConstantType)
                    checks.append(attr)

    def test_repr(self):
        class Alphanum(Constants):
            greek = True
            class Alpha:
                alpha = 'a'
                beta = 'b'
                gamma = 'c'
            class Num:
                alpha = 1
                beta = 2
                gamma = 3
        output = """\
Alphanum:
    Alpha:
        alpha: 'a'
        beta: 'b'
        gamma: 'c'
    Num:
        alpha: 1
        beta: 2
        gamma: 3
    greek: True
"""
        self.assertEqual(repr(Alphanum), output)
        self.assertEqual(str(Alphanum), output)


class PathSegmentsTestCase(RemoteTestCase):
    def setUp(self):
        self.segments = ['alpha', 'beta', 'gamma']
        self.defaults = ['0', '1', '2']
        self.url = URL('', '/', self.segments, self.defaults)

    def test_attributes(self):
        other_segments = ['one', 'two', 'three']
        other_url = URL('', '/', other_segments, self.defaults)
        for segment, other_segment in zip(self.segments, other_segments):
            self.assertTrue(hasattr(self.url, segment))
            self.assertFalse(hasattr(other_url, segment))
            self.assertTrue(hasattr(other_url, other_segment))
            self.assertFalse(hasattr(self.url, other_segment))

    def test_propierties(self):
        self.assertEqual(str(self.url), '/0/1/2')
        self.url.alpha = '9'
        self.url.beta = '8'
        self.url.gamma = '7'
        self.assertEqual(str(self.url), '/9/8/7')


class ParsingTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def test_items(self):
        self.assertEqual(len(list(self.torrents.items())), 30)
        self.assertEqual(len(list(iter(self.torrents))), 30)

    def test_torrent_rows(self):
        request = urlopen(str(self.torrents.url))
        content = request.read()
        page = BeautifulSoup(content)
        rows = self.torrents._get_torrent_rows(page)
        self.assertEqual(len(rows), 30)

    def test_torrent_build(self):
        pass


class TorrentTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def assertEqualDatetimes(self, *datetimes):
        datetimes = [ d.replace(microsecond=0) for d in datetimes ]
        return self.assertEqual(*datetimes)

    def test_created_timestamp_parse(self):
        for torrent in self.torrents.items():
            torrent.created
        torrent._created = '1 sec ago'
        self.assertEqualDatetimes(torrent.created, datetime.now() - timedelta(seconds=1))
        torrent._created = '1 min ago'
        self.assertEqualDatetimes(torrent.created, datetime.now() - timedelta(minutes=1))
        torrent._created = '1 hour ago'
        self.assertEqualDatetimes(torrent.created, datetime.now() - timedelta(hours=1))
        torrent._created = 'Today'
        self.assertEqual(torrent.created.date(), datetime.now().date())



class PaginationTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def test_page_items(self):
        self.assertEqual(len(list(self.torrents.items())), 30)

    def test_multipage_items(self):
        self.torrents.multipage()
        items = itertools.islice(self.torrents.items(), 100)
        self.assertEqual(len(list(items)), 100)
        self.assertEqual(self.torrents.page(), 3)

    def test_last_page(self):
        class DummyList(List):
            pages_left = 5
            def items(self):
                if self.pages_left == 0:
                    raise StopIteration()
                for i in range(10):
                    yield i
                self.pages_left -= 1
        class DummySearch(Search, Paginated, DummyList):
            pass
        self.torrents = DummySearch(self.url, 'breaking bad').multipage()
        self.assertEqual(len(list(iter(self.torrents))), 50)


class SearchTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def test_url(self):
        self.assertEqual(str(self.torrents.url),
                self.url + '/search/breaking%20bad/0/7/0')
        self.torrents.query('something').page(1).next().previous()
        self.torrents.order(9).category(100)
        self.assertEqual(self.torrents.query(), 'something')
        self.assertEqual(self.torrents.page(), 1)
        self.assertEqual(self.torrents.order(), 9)
        self.assertEqual(self.torrents.category(), 100)
        self.assertEqual(str(self.torrents.url),
                self.url + '/search/something/1/9/100')

    def test_torrents(self):
        for item in self.torrents:
            self.assertEqual(unicode, type(item.title))
            self.assertEqual(unicode, type(item.user))
            self.assertTrue(hasattr(item, 'url'))
            # ensure the URL points to the /torrent/ html page
            self.assertTrue(item.url.path().startswith('/torrent/'))


class RecentTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Recent(self.url)

    def test_url(self):
        self.assertEqual(str(self.torrents.url),
                self.url + '/recent/0')
        self.torrents.page(1).next().previous()
        self.assertEqual(str(self.torrents.url),
                self.url + '/recent/1')


class TopTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Top(self.url)

    def test_url(self):
        self.assertEqual(str(self.torrents.url),
                self.url + '/top/0')
        self.torrents.category(100)
        self.assertEqual(str(self.torrents.url),
                self.url + '/top/100')


class TPBTestCase(RemoteTestCase):
    def setUp(self):
        self.tpb = TPB(self.url)

    def test_search(self):
        kwargs = {'query': 'breaking bad', 'page': 5, 'order': 9, 'category': 100}
        a_search = self.tpb.search(**kwargs)
        b_search = Search(self.url, **kwargs)
        self.assertTrue(isinstance(a_search, Search))
        self.assertTrue(isinstance(b_search, Search))
        self.assertEqual(str(a_search.url), str(b_search.url))

    def test_recent(self):
        kwargs = {'page': 5}
        a_recent = self.tpb.recent(**kwargs)
        b_recent = Recent(self.url, **kwargs)
        self.assertTrue(isinstance(a_recent, Recent))
        self.assertTrue(isinstance(b_recent, Recent))
        self.assertEqual(str(a_recent.url), str(b_recent.url))

    def test_top(self):
        kwargs = {'category': 100}
        a_top = self.tpb.top(**kwargs)
        b_top = Top(self.url, **kwargs)
        self.assertTrue(isinstance(a_top, Top))
        self.assertTrue(isinstance(b_top, Top))
        self.assertEqual(str(a_top.url), str(b_top.url))


def load_tests(loader, tests, discovery):
    for attr, envvar in [('_do_local', 'LOCAL'), ('_do_remote', 'REMOTE')]:
        envvar = os.environ.get(envvar)
        if envvar is not None:
            setattr(RemoteTestCase, attr, envvar.lower() in ['true', '1'])
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    unittest.main()
