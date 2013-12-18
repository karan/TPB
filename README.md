![TPB](http://www.goel.im/images/tpb.jpg)

Unofficial Python API for [ThePirateBay](http://thepiratebay.gy/).

| Build Status | Test Coverage |
| ------------ | ------------- |
| [![Build Status](https://travis-ci.org/karan/TPB.png)](https://travis-ci.org/karan/TPB) | [![Coverage Status](https://coveralls.io/repos/karan/TPB/badge.png)](https://coveralls.io/r/karan/TPB) |

Installation
=============

    $ pip install ThePirateBay

Note that ``ThePirateBay`` depends on ``lxml``. If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

Usage
==========

    from tpb import TPB
    from tpb import CATEGORIES, ORDERS

    t = TPB('https://thepiratebay.gy') # create a TPB object with default domain

    # search for 'public domain' in 'movies' category
    search = t.search('public domain', category=CATEGORIES.VIDEO.MOVIES)

    # return listings from page 2 of this search
    search.page(2)

    # sort this search by count of seeders, and return a multipage result
    search.order(ORDERS.SEEDERS.ASC).multipage()

    # search, order by seeders and return page 3 results
    t.search('python').order(ORDERS.SEEDERS.ASC).page(3)

    # multipage beginning on page 4
    t.search('recipe book').page(4).multipage()

    # search, in a category and return multipage results
    t.search('something').category(CATEGORIES.OTHER.OTHER).multipage()

    # get page 3 of recent torrents
    t.recent().page(3)

    # get top torrents in Movies category
    t.top().category(CATEGORIES.VIDEO.MOVIES)

    # print all torrent descriptions
    for torrent in torrent.search('public domain'):
        print(torrent.info)

    # print all torrent files and their sizes
    for torrent in torrent.search('public domain'):
        print(torrent.files)

![](https://blockchain.info/Resources/buttons/donate_64.png)
=============

If TPB API has helped you in any way, and you'd like to help the developer, please consider donating.

**- BTC: [19dLDL4ax7xRmMiGDAbkizh6WA6Yei2zP5](http://i.imgur.com/bAQgKLN.png)** *Link to QR code*

**- Flattr: [https://flattr.com/profile/thekarangoel](https://flattr.com/profile/thekarangoel)**


Torrent details available
==================

Attributes
----------

* **title** # the title of the torrent
* **url** # TPB url for the torrent
* **category** # the main category
* **sub_category** # the sub category
* **magnet_link** # magnet download link
* **torrent_link** # .torrent download link
* **created** # uploaded date time
* **size** # size of torrent
* **user** # username of uploader
* **seeders** # number of seeders
* **leechers** # number of leechers

Properties
----------

* **created** # creation date -- parsed when accessed
* **info** # detailed torrent description -- *needs separate request*
* **files** # dictionary of files and their size -- *needs separate request*

Tests
=====

You need `bottle` and `testscenarios` installed to run the tests.

    $ pip install -r tests/requirements.txt

To execute the tests simply run:

    $ python -m unittest discover

By default the tests are ran on a local test server with predownloaded original
responses. You can activate the remote running option by:

    $ REMOTE=true python -m unittest discover


Contribute
========

If you want to add any new features, or improve existing ones, feel free to send a pull request!


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/karan/tpb/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

