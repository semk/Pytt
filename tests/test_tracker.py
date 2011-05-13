#!/usr/bin/env python
#
# Common utilities for Pytt.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com


import os
import sys
from nose import with_setup
import subprocess
import urllib2
import urllib
import hashlib

sys.path.append('../')
from pytt.bencode import bencode


def start_tracker():
    tracker = os.path.abspath('../pytt/tracker.py')
    subprocess.Popen(['python', tracker])


def stop_tracker():
    raise KeyboardInterrupt


@with_setup(start_tracker, stop_tracker)
def test_tracker():
    pass


if __name__ == '__main__':
    info = {'piece length': 1024,
            'pieces': hashlib.sha1('crap').hexdigest(),
            'private': 0
            }
    bencoded_info = bencode(info)
    info_hash = hashlib.sha1(bencoded_info).hexdigest()
    query = {'info_hash': info_hash,
             'peer_id': 'BitTorrent-1.0',
             'ip': '112.113.144.1',
             'port': '6881'
             }
    query = urllib.urlencode(query)
    res = urllib2.urlopen('http://127.0.0.1:8080/announce?%s' %query)
    print res