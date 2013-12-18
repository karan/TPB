#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ThePirateBay',
    version='1.3.0',
    install_requires=['purl', 'dateutils', 'lxml', 'cssselect'],
    author='Karan Goel',
    author_email='karan@goel.im',
    packages=['tpb','tests'],
    test_suite='tests',
    url='https://github.com/thekarangoel/TPB/',
    license='MIT License',
    description='Unofficial Python API for ThePirateBay.',
    long_description='Unofficial Python API for ThePirateBay. Usage: https://github.com/thekarangoel/TPB.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Utilities',
    ],
)
