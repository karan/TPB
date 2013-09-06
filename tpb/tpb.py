#!/usr/bin/env python

"""
Unofficial Python API for ThePirateBay.
Currently supports searching, recent torrents and top 100 torrents.

@author Karan Goel
@email karan@goel.im


Copyright (C) 2013  Karan Goel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

import os
import re
import urllib
from functools import wraps

from purl import URL
from bs4 import BeautifulSoup


def self_if_not_none(func):
    @wraps(func)
    def wrapper(self, arg=None):
        result = func(self, arg)
        if arg is None:
            return result
        else:
            return self
    return wrapper


class List(object):
    """
    Abstract class for parsing a torrent list at some url and generate torrent 
    objects to iterate over. Includes a resource path parser.
    """

    _meta = re.compile('Uploaded (.*), Size (.*), ULed by (.*)')
    base_path = ''

    def __init__(self, base_url):
        self.url = base_url.add_path_segment(self.base_path)

    def _parse_path(self, *defaults):
        """
        Strip the latest len(defaults) segments of self.url and replace them
        with defaults, then return the latest len(defaults) segments. If some
        argument is None, the segment is not replaced.
        """
        segments = self.url.path_segments()
        length = len(defaults)
        before = list(segments[:-length])
        after = segments[-length:]
        after = [ seg if defaults[i] is None else defaults[i] \
                for i, seg in enumerate(after) ]
        after = [ str(seg) for seg in after ]
        self.url = self.url.path_segments(before + after)
        return after

    def items(self):
        """
        Request self.url and parse response. Yield a Torrent object for every
        torrent on page.
        """
        request = urllib.urlopen(self.url.as_string())
        content = request.read()
        page = BeautifulSoup(content)
        for row in self._get_torrent_rows(page):
            yield self._build_torrent(row)

    def __iter__(self):
        return self.items()

    def _get_torrent_rows(self, page):
        """
        Returns all 'tr' tag rows as a list of tuples. Each tuple is for
        a single torrent.
        """
        table = page.find('table') # the table with all torrent listing
        return table.findAll('tr')[1:-1] # get all rows but header, pagination
    
    def _build_torrent(self, row):
        """
        Builds and returns a Torrent object for the given parsed row.
        """
        # Scrape, strip and build!!!
        cols = row.findAll('td') # split the row into it's columns
        
        # this column contains the categories
        cat_col = cols[0].findAll('a')
        [category, sub_category] = [c.string for c in cat_col]
        
        # this column with all important info
        links = cols[1].findAll('a') # get 4 a tags from this columns
        title = unicode(links[0].string.encode('utf8')) # title of the torrent
        url = self.url.add_path_segment(links[0].get('href'))
        magnet_link = links[1].get('href') # the magnet download link
        try:
            torrent_link = links[2].get('href') # the torrent download link
            if not torrent_link.endswith('.torrent'):
                torrent_link = None
        except IndexError:
            torrent_link = None

        meta_col = cols[1].find('font').text # don't need user
        match = self._meta.match(meta_col)
        created = match.groups()[0].replace(u'\xa0',u' ')
        size = match.groups()[1].replace(u'\xa0',u' ')
        user = unicode(match.groups()[2].encode('utf8')) # uploaded by user
        
        # last 2 columns for seeders and leechers
        seeders = int(cols[2].string)
        leechers = int(cols[3].string)
        
        t = Torrent(title, url, category, sub_category, magnet_link,
                    torrent_link, created, size, user, seeders, leechers)
        return t


class Paginated(List):
    """
    Abstract class on top of List for parsing a torrent list with pagination 
    capabilities. 
    """
    def __init__(self, *args, **kwargs):
        super(Paginated, self).__init__(*args, **kwargs)
        self._multipage = False

    def items(self):
        """
        Request self.url and parse response. Yield a Torrent object for every
        torrent on page. If self._multipage is True, Torrents from next pages 
        are automatically chained.
        """
        if self._multipage:
            while True: #TODO: raise StopIteration on last page
                for item in super(Paginated, self).items():
                    yield item
                self.next()
        else:
            for item in super(Paginated, self).items():
                yield item

    def multipage(self):
        """
        Enable multipage iteration.
        """
        self._multipage = True
        return self

    def page(self, number=None):
        self._multipage = False

    def next(self):
        """
        Request the next page.
        """
        self.page(self.page() + 1)


class Search(Paginated):
    """
    Paginated search including query, category and ordering management.
    """
    base_path = 'search/query/page/ordering/category'

    def __init__(self, base_url, query, page=0, ordering=7, category=0):
        super(Search, self).__init__(base_url)
        self.path(query, page, ordering, category)

    def path(self, query=None, page=None, ordering=None, category=None):
        return self._parse_path(query, page, ordering, category)

    @self_if_not_none
    def query(self, query=None):
        """
        If query is given, modify query segment of url with it, return actual
        query segment otherwise.
        """
        return self.path(query=query)[0]

    @self_if_not_none
    def page(self, number=None):
        """
        If path is given, modify path segment of url with it, return actual
        path segment otherwise. Disables multipage iteration.
        """
        super(Search, self).page(number)
        return int(self.path(page=number)[1])

    @self_if_not_none
    def order(self, ordering=None):
        """
        If ordering is given, modify order segment of url with it, return actual
        order segment otherwise.
        """
        return int(self.path(ordering=ordering)[2])

    @self_if_not_none
    def category(self, category=None):
        """
        If category is given, modify category segment of url with it, return 
        actual category segment otherwise.
        """
        return int(self.path(category=category)[3])


class Recent(Paginated):
    """
    Paginated most recent torrents.
    """
    base_path = 'recent/page'

    def __init__(self, base_url, page=0):
        super(Recent, self).__init__(base_url)
        self.path(page)

    def path(self, page=None):
        return self._parse_path(page)

    @self_if_not_none
    def page(self, number=None):
        """
        If path is given, modify path segment of url with it, return actual
        path segment otherwise. Disables multipage iteration.
        """
        super(Recent, self).page(number)
        return int(self.path(page=number)[0])


class Top(List):
    """
    Top torrents with category management.
    """
    base_path = 'top/category'

    def __init__(self, base_url, category=0):
        super(Top, self).__init__(base_url)
        self.path(category)

    def path(self, category=None):
        self._parse_path(category)

    @self_if_not_none
    def category(self, category=None):
        """
        If category is given, modify category segment of url with it, return 
        actual category segment otherwise.
        """
        return self.path(category=category)[0]


class TPB(object):
    """
    TPB API with searching, most recent torrents and top torrents support.
    Passes on base_url to the instantiated Search, Recent and Top classes.
    """
    
    def __init__(self, base_url):
        self.base_url = URL(base_url)

    def search(self, query, page=0, order=7, category=0, multipage=False):
        """
        Searches TPB for query and return a list of Torrents.
        """
        search = Search(self.base_url, query, page, order, category)
        if multipage:
            search.multipage()
        return search

    def recent(self, page=0):
        """
        Most recent Torrents added to TPB.
        """
        return Recent(self.base_url, page)

    def top(self, category=0):
        """
        Top Torrents on TPB.
        """
        return Top(self.base_url, category)
    

class Torrent():
    """
    Represents one single torrent on TPB.
    """
    
    def __init__(self, title, url, category, sub_category, magnet_link,
                 torrent_link, created, size, user, seeders, leechers):
        self.title = title # the title of the torrent
        self.url = url # TPB url for the torrent
        self.category = category # the main category
        self.sub_category = sub_category # the sub category
        self.magnet_link = magnet_link # magnet download link
        self.torrent_link = torrent_link # .torrent download link
        self.created = created # uploaded date time
        self.size = size # size of torrent
        self.user = user # username of uploader
        self.seeders = seeders # number of seeders
        self.leechers = leechers # number of leechers
    
    def print_torrent(self):
        """
        Print the details of a torrent
        """
        print 'Title: %s' % self.title
        print 'URL: %s' % self.url
        print 'Category: %s' % self.category
        print 'Sub-Category: %s' % self.sub_category
        print 'Magnet Link: %s' % self.magnet_link
        print 'Torrent Link: %s' % self.torrent_link
        print 'Uploaded: %s' % self.created
        print 'Size: %s' % self.size
        print 'User: %s' % self.user
        print 'Seeders: %d' % self.seeders
        print 'Leechers: %d' % self.leechers
    
    def __repr__(self):
        return '{0} by {1}'.format(self.title, self.user)
