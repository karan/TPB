#!/usr/bin/env python

"""
Unofficial Python API for ThePirateBay.

@author Karan Goel
@email karan@goel.im
"""

from __future__ import unicode_literals

import datetime
import dateutil.parser
from functools import wraps
import os
import re
import sys
import time

from bs4 import BeautifulSoup

from .utils import URL

if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    unicode = str
else:
    from urllib2 import urlopen


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

    def items(self):
        """
        Request self.url and parse response. Yield a Torrent object for every
        torrent on page.
        """
        request = urlopen(str(self.url))
        content = request.read()
        page = BeautifulSoup(content, "lxml")
        for row in self._get_torrent_rows(page):
            yield self._build_torrent(row)

    def __iter__(self):
        return self.items()

    def _get_torrent_rows(self, page):
        """
        Returns all 'tr' tag rows as a list of tuples. Each tuple is for
        a single torrent.
        """
        table = page.find('table')  # the table with all torrent listing
        if table is None:  # no table means no results:
            return []
        else:
            return table.findAll('tr')[1:31]  # get all rows but header, pagination

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
        title = unicode(links[0].string)
        url = self.url.build().path(links[0].get('href'))
        magnet_link = links[1].get('href') # the magnet download link
        try:
            torrent_link = links[2].get('href') # the torrent download link
            if not torrent_link.endswith('.torrent'):
                torrent_link = None
        except IndexError:
            torrent_link = None

        meta_col = cols[1].find('font').text # don't need user
        match = self._meta.match(meta_col)
        created = match.groups()[0].replace('\xa0', ' ')
        size = match.groups()[1].replace('\xa0', ' ')
        user = match.groups()[2]  # uploaded by user

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
            while True:
                items = super(Paginated, self).items()
                first = next(items, None)
                if first is None:
                    raise StopIteration()
                else:
                    yield first
                    for item in items:
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

    @self_if_not_none
    def page(self, number=None):
        if number is None:
            return int(self.url.page)
        self.url.page = str(number)

    def next(self):
        """
        Request the next page.
        """
        self.page(self.page() + 1)
        return self

    def previous(self):
        """
        Request previous page.
        """
        self.page(self.page() - 1)
        return self


class Search(Paginated):
    """
    Paginated search including query, category and order management.
    """
    base_path = '/search'

    def __init__(self, base_url, query, page='0', order='7', category='0'):
        super(Search, self).__init__()
        self.url = URL(base_url, self.base_path,
                        segments=['query', 'page', 'order', 'category'],
                        defaults=[query, str(page), str(order), str(category)],
                        )

    @self_if_not_none
    def query(self, query=None):
        """
        If query is given, modify query segment of url with it, return actual
        query segment otherwise.
        """
        if query is None:
            return self.url.query
        self.url.query = query

    @self_if_not_none
    def order(self, order=None):
        """
        If order is given, modify order segment of url with it, return actual
        order segment otherwise.
        """
        if order is None:
            return int(self.url.order)
        self.url.order = str(order)

    @self_if_not_none
    def category(self, category=None):
        """
        If category is given, modify category segment of url with it, return
        actual category segment otherwise.
        """
        if category is None:
            return int(self.url.category)
        self.url.category = str(category)


class Recent(Paginated):
    """
    Paginated most recent torrents.
    """
    base_path = '/recent'

    def __init__(self, base_url, page='0'):
        super(Recent, self).__init__()
        self.url = URL(base_url, self.base_path,
                        segments=['page'],
                        defaults=[str(page)],
                        )


class Top(List):
    """
    Top torrents with category management.
    """
    base_path = '/top'

    def __init__(self, base_url, category='0'):
        self.url = URL(base_url, self.base_path,
                        segments=['category'],
                        defaults=[str(category)],
                        )

    @self_if_not_none
    def category(self, category=None):
        """
        If category is given, modify category segment of url with it, return
        actual category segment otherwise.
        """
        if category is None:
            return int(self.url.category)
        self.url.category = str(category)


class TPB(object):
    """
    TPB API with searching, most recent torrents and top torrents support.
    Passes on base_url to the instantiated Search, Recent and Top classes.
    """

    def __init__(self, base_url):
        self.base_url = base_url

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
        self._created = created # uploaded date time
        self.size = size # size of torrent
        self.user = user # username of uploader
        self.seeders = seeders # number of seeders
        self.leechers = leechers # number of leechers

    @property
    def created(self):
        timestamp = self._created
        if timestamp.endswith('ago'):
            quantity, kind, ago = timestamp.split()
            quantity = int(quantity)
            current = time.time()
            if 'sec' in kind:
                current -= quantity
            elif 'min' in kind:
                current -= quantity * 60
            elif 'hour' in kind:
                current -= quantity * 60 * 60
            return datetime.datetime.fromtimestamp(current)
        timestamp = timestamp.replace('Today', datetime.date.today().isoformat())
        try:
            return dateutil.parser.parse(timestamp)
        except:
            return datetime.datetime.now()

    def print_torrent(self):
        """
        Print the details of a torrent
        """
        print('Title: %s' % self.title)
        print('URL: %s' % self.url)
        print('Category: %s' % self.category)
        print('Sub-Category: %s' % self.sub_category)
        print('Magnet Link: %s' % self.magnet_link)
        print('Torrent Link: %s' % self.torrent_link)
        print('Uploaded: %s' % self.created)
        print('Size: %s' % self.size)
        print('User: %s' % self.user)
        print('Seeders: %d' % self.seeders)
        print('Leechers: %d' % self.leechers)

    def __repr__(self):
        return '{0} by {1}'.format(self.title, self.user)
