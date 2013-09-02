#!/usr/bin/env python

from tpb import TPB

t = TPB()

"""
for to in t.get_recent_torrents():
    print '*' * 50
    to.print_torrent()
    print '\n'
"""

results = t.search('hello world')

for r in results:
    print '*' * 50
    r.print_torrent()
    print '\n'
