![TPB](http://www.goel.im/images/tpb.jpg)

Unofficial Python API for [ThePirateBay](http://thepiratebay.pe/).

| Build Status | Test Coverage | Version | Download |
| ------------ | ------------- | ------- | -------- |
| [![Build Status](https://travis-ci.org/karan/TPB.png)](https://travis-ci.org/karan/TPB) | [![Coverage Status](https://coveralls.io/repos/karan/TPB/badge.png)](https://coveralls.io/r/karan/TPB) | [![Version](https://pypip.in/v/ThePirateBay/badge.png)](https://crate.io/packages/ThePirateBay/) | [![Downloads](https://pypip.in/d/ThePirateBay/badge.png)](https://crate.io/packages/ThePirateBay/) |

Installation
=============

    $ pip install ThePirateBay

Note that ``ThePirateBay`` depends on ``lxml``. If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

[Donate](https://www.gittip.com/Karan%20Goel/)
=============

If you love and use *TPB*, please consider [donating via gittip](https://www.gittip.com/Karan%20Goel/). Any support is appreciated!


Usage
==========

    from tpb import TPB
    from tpb import CATEGORIES, ORDERS

    t = TPB('https://thepiratebay.pe') # create a TPB object with default domain

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

Torrent details available
==================

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

