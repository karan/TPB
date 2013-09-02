![TPB](http://www.goel.im/images/tpb.jpg)

Unofficial Python API for [ThePirateBay](http://thepiratebay.sx/).

[![Version](https://pypip.in/v/ThePirateBay/badge.png)](https://crate.io/packages/ThePirateBay/)   [![Downloads](https://pypip.in/d/ThePirateBay/badge.png)](https://crate.io/packages/ThePirateBay/)

Installation
=============

    $ pip install ThePirateBay


[Donate](https://www.gittip.com/Karan%20Goel/)
=============

If you love and use *TPB*, please consider [donating via gittip](https://www.gittip.com/Karan%20Goel/). Any support is appreciated!


Classes
==========

## `TPB`

The class that parses the torrent listing page, and builds up all Torrent objects.

#### Methods

`set_url(url)` - Sets the base URL when TPB changes domain and/or using a proxy.

`get_recent_torrents()` - Returns a list of Torrent objects from the 'recent' page of TPB

`search(query, category=0)` - Searches TPB for the passed query and returns a list of Torrents

## `Torrent`

Represents one single torrent on TPB

#### Methods

`print_torrent()` - Print the details of a torrent

#### Story details

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
        
Contribute
========

If you want to add any new features, or improve existing ones, feel free to send a pull request!