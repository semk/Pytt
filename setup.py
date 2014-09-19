#!/usr/bin/env python
#
# Pytt: BitTorrent Tracker using Tornado
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com

from setuptools import setup, find_packages

setup(
    name = "Pytt",
    version = "0.1.7",
    packages = find_packages(),
    install_requires = ['setuptools',
                        'tornado >= 4.0',
                        ],
    extras_require = {'test': ['nose']},
    scripts = ['scripts/pytt'],

    # metadata for upload to PyPI
    author = "Sreejith K",
    author_email = "sreejithemk@gmail.com",
    description = "A Pure Python BitTorrent Tracker using Tornado",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    keywords = "bittorrent tracker bencode bdecode scrape ui",
    url = "http://foobarnbaz.com/lab/pytt",
    zip_safe = True,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Tornado"
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    long_description = """Pytt is a simple BitTorrent tracker written
                        using Tornado non-blocking web server.
                        It also features a UI for showing tracker statistics.""",
)
