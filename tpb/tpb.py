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


import re
import urllib

from bs4 import BeautifulSoup


class TPB():
    """
    The class that parses the torrent listing page, and builds up
    all Torrent objects.
    """
    
    base_url = 'https://thepiratebay.sx' # could change!!!
    
    def set_url(self, url):
        """
        Sets the base URL when TPB changes domain and/or using a proxy.
        """
        global base_url
        base_url = url
    
    
    def get_soup(self, page=''):
        """
        Returns a bs4 object of the page requested. page can be:
        
        'recent'
        a 'search' page
        a 'top' page
        """
        content = urllib.urlopen('%s/%s' % (base_url, page)).read()
        return BeautifulSoup(content)
    
    
    def get_torrents_rows(self, soup):
        """
        Returns all 'tr' tag rows as a list of tuples. Each tuple is for
        a single torrent.
        """
        table = soup.find('table') # the table with all torrent listing
        return table.findAll('tr')[1:-1] # get all rows but header, pagination
    
    def build_torrent(self, all_rows):
        """
        Builds and returns a list of Torrent objects from
        the passed source.
        """
        all_torrents = [] # list to hold all torrents
        
        for row in all_rows:
            # Scrape, strip and build!!!
            cols = row.findAll('td') # split the row into it's columns
            
            # this column contains the categories
            cat_col = cols[0].findAll('a')
            [category, sub_category] = [c.string for c in cat_col]
            
            # this column with all important info
            links = cols[1].findAll('a') # get 4 a tags from this columns
            title = links[0].string # title of the torrent
            url = '%s/%s' % (base_url, links[0].get('href'))
            magnet_link = links[1].get('href') # the magnet download link
            torrent_link = links[2].get('href') # the .torrent download link
            
            meta_col = cols[1].find('font').text # don't need user
            pat = re.compile('Uploaded (.*), Size (.*), ULed by (.*)')
            match = re.match(pat, meta_col)
            created = match.groups()[0]
            size = match.groups()[1].replace(u'\xa0',u' ')
            user = match.groups()[2] # uploaded by user
            
            # last 2 columns for seeders and leechers
            seeders = int(cols[2].string)
            leechers = int(cols[3].string)
            
            t = Torrent(title, url, category, sub_category, magnet_link,
                        torrent_link, created, size, user, seeders, leechers)
            all_torrents.append(t)
        
        return all_torrents

    def get_recent_torrents(self):
        """
        Returns a list of Torrent objects from the 'recent' page of TPB
        """
        all_rows = self.get_torrents_rows(
            self.get_soup(page='recent')
            )
        return self.build_torrent(all_rows)

    def search(self, query, category=0):
        """
        Searches TPB for the passed query and returns a list of Torrents.
        
        category is an int with one of the following values:
        0 - all
        100 - audio
            101 - Music, 102 - Audio books, 103 - Sound clips, 104 - FLAC,
            199 - Other
        200 - Video
            201 - Movies, 202 - Movies DVDR, 203 - Music videos,
            204 - Movie clips, 205 - TV shows, 206 - Handheld,
            207 - HD - Movies, 208 - HD - TV shows, 209 - 3D, 299 - Other
        300 - Applications
            301 - Windows, 302 - Mac, 303 - UNIX, 304 - Handheld,
            305 - IOS (iPad/iPhone), 306 - Android, 399 - Other OS
        400 - Games
            401 - PC, 402 - Mac, 403 - PSx, 404 - XBOX360, 405 - Wii,
            406 - Handheld, 407 - IOS (iPad/iPhone), 408 - Android,
            499 - Other
        500 - Other
            601 - E-books, 602 - Comics, 603 - Pictures, 604 - Covers,
            605 - Physibles, 699 - Other
        """
        all_rows = self.get_torrents_rows(
            self.get_soup(page='search/{0}/0/99/{1}'.format(
                urllib.quote(query),
                category
                ))
            )
        return self.build_torrent(all_rows)
    

class Torrent():
    """
    Represents one single torrent on TPB
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
        """
        A string representation of the class object
        """
        return '{0} by {1}'.format(self.title, self.user)