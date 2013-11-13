### master

* Fix: bug in torrent creation timestamp parsing
* Fix: ascending and descending ordering confusion
* Fix: default to only local testing
* Add: docs about possible problems with ``lxml``s dependency compilations

### v1.1.3

* Add: Support for searches that do not return any results
* Add: Py 3 support
* Fix: Correct UTF-8 handling

### v1.1.2

* Move to MIT License

### v1.1.1

* Fix: Make BeautifulSoup use lxml to avoid bad html parsing errors

### v1.1.0

* Add: coveralls (coverage reporting service) support
* Add: full python 3.2 and python 3.3 support.
* Add: Local (bottle server with presets) and remote testing.
* Add: Last page handling in multipage mode.
* Fix: Chained path modification bugs.
* Add: Torrent creation date parsing.
* Add: Travis CI support.
* Add: requirements.txt for tests.
* Add: Authors file.
* Rewrite: Smart url handling.
* Rewrite: Multiple scenario testing with testscenarios.

### v1.0.0

* Add: Development tests
* Fix: `NoneType` on Recent torrents

### v0.0.5

* Add: Ordering/sorting
* Add: Advanced pagination
* Add: Getting top torrents
* Rewrite: Category search

### v0.0.4

* Fix: `UnicodeEncodeError` thrown by `created` field.
* Fix: `IndexError` issue #11
