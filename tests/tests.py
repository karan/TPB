import unittest
import urllib

from bs4 import BeautifulSoup

from cases import RemoteTestCase
from tpb.tpb import List, Search


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
        self.assertItemsEqual(self.torrents.url.path_segments(), result)
        for change in range(len(changes)):
            changes[change] = 'changed'
            result[change] = 'changed'
            self.torrents._parse_path(*changes)
            self.assertItemsEqual(self.torrents.url.path_segments(), result)


class ParsingTestCase(RemoteTestCase):
    def test_torrent_rows(self):
        torrents = Search(self.url, 'breaking bad')
        request = urllib.urlopen(torrents.url.as_string())
        content = request.read()
        page = BeautifulSoup(content)
        rows = torrents._get_torrent_rows(page)
        self.assertEqual(len(rows), 30)

    def test_torrent_build(self):
        pass


class PaginationTestCase(RemoteTestCase):
    pass


class SearchTestCase(RemoteTestCase):
    pass


class RecentTestCase(RemoteTestCase):
    pass


class TopTestCase(RemoteTestCase):
    pass


if __name__ == '__main__':
    unittest.main()
