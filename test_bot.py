#!/usr/bin/env python

from tpb import TPB
from tpb import CATEGORIES, ORDERS

t = TPB('https://thepiratebay.sx') # create a TPB object with default domain

# search for 'breaking bad' in 'movies' category
# search = t.search('breaking bad', category=CATEGORIES.VIDEO.MOVIES)

# return listings from page 2 of this search
# search.page(2)

# sort this search by count of seeders, and return a multipage result
# search.order(ORDERS.SEEDERS).multipage()

# search, order by seeders and return page 3 results
# t.search('breaking bad').order(ORDERS.SEEDERS).page(3)

# multipage beginning on page 4
# t.search('babylon 5').page(4).multipage()

# search, in a category and return multipage results
# t.search('something').category(CATEGORIES.OTHERS).multipage()

# get page 3 of recent torrents
rec = t.recent().page(3)
for r in rec:
    print r


# get top torrents in Movies category
# t.top().category(CATEGORIES.MOVIES)