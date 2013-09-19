import sys
import unittest
import itertools

from bs4 import BeautifulSoup

from tpb.tpb import List, Search, Recent, Top

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from tests.cases import RemoteTestCase
else:
    from urllib2 import urlopen
    from cases import RemoteTestCase



class ConstantsTestCase(RemoteTestCase):
    pass


class PathSegmentsTestCase(RemoteTestCase):
    def setUp(self):
        segments = 'one/two/three/four/five'.split('/')
        self.torrents = List(self.url)
        self.torrents.url = self.torrents.url.path_segments(segments)

    def test_get_segments(self):
        result = []
        for segment in self.torrents.url.path_segments()[::-1]:
            result.insert(0, segment)
            self.assertEqual(self.torrents._parse_path(*[None]*len(result)), result)

    def test_set_segments(self):
        result = list(self.torrents.url.path_segments())
        changes = [None]*len(result)
        self.torrents._parse_path(*changes)
        self._assertCountEqual(self.torrents.url.path_segments(), result)
        for change in range(len(changes)):
            changes[change] = 'changed'
            result[change] = 'changed'
            self.torrents._parse_path(*changes)
            self._assertCountEqual(self.torrents.url.path_segments(), result)


class ParsingTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def test_items(self):
        self.assertEqual(len(list(self.torrents.items())), 30)

    def test_torrent_rows(self):
        request = urlopen(self.torrents.url.as_string())
        content = request.read()
        page = BeautifulSoup(content)
        rows = self.torrents._get_torrent_rows(page)
        self.assertEqual(len(rows), 30)

    def test_torrent_build(self):
        pass


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


class SearchTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Search(self.url, 'breaking bad')

    def test_url(self):
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/search/breaking%20bad/0/7/0')
        self.torrents.query('something').page(1).next().previous()
        self.torrents.order(9).category(100)
        self.assertEqual(self.torrents.query(), 'something')
        self.assertEqual(self.torrents.page(), 1)
        self.assertEqual(self.torrents.order(), 9)
        self.assertEqual(self.torrents.category(), 100)
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/search/something/1/9/100')


class RecentTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Recent(self.url)

    def test_url(self):
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/recent/0')
        self.torrents.page(1).next().previous()
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/recent/1')


class TopTestCase(RemoteTestCase):
    def setUp(self):
        self.torrents = Top(self.url)

    def test_url(self):
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/top/0')
        self.torrents.category(100)
        self.assertEqual(self.torrents.url.as_string(),
                self.url + '/top/100')



if __name__ == '__main__':
    if '--local' in sys.argv:
        sys.argv.remove('--local')
        RemoteTestCase._is_remote_available = False
    unittest.main()
