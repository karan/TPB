#!/usr/bin/env python

from tpb import TPB

t = TPB()

# when using a proxy site
# t.set_url('http://uberproxy.net/thepiratebay.sx')


for to in t.get_recent_torrents():
    print '*' * 50
    to.print_torrent()
    print '\n'

"""
# search for programming ebooks
results = t.search('hello world', category=601)

for r in results:
    print '*' * 50
    r.print_torrent()
    print '\n'
"""