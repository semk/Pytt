#!/usr/bin/env python
#
# TestCases for Pytt Tracker 
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com


import os
import sys
from nose import with_setup
import urllib2
import urllib
import hashlib
from tornado.testing import AsyncHTTPTestCase

sys.path.append('../')
from pytt.tracker import *


# define application
app = tornado.web.Application([
            (r"/announce.*", AnnounceHandler),
            (r"/scrape.*", ScrapeHandler),
            (r"/", TrackerStats),
        ])


def clear_db():
    """Clear the tracker db.
    """
    try:
        os.remove(DB_PATH)
    except:
        pass


class TestHandlerBase(AsyncHTTPTestCase):
    """Base Test class for all request handlers.
    """
    def setUp(self):
        """Do this before every test
        """
        clear_db()
        super(TestHandlerBase, self).setUp()

    def get_app(self):
        """Get the application object
        """
        return app

    def get_http_port(self):
        """Set Tracker listen port from config or default 8080
        """
        return get_config().getint('tracker', 'port') or 8080


class TestAnnounceHandler(TestHandlerBase):
    """Test cases for Announce request for the Torrent Tracker
    """
    def announce_test(self):
        """Test response for Announce.
        """
        # torrent meta info
        info = {'piece length': 1024,
                'pieces': hashlib.sha1('crap').digest(),
                'private': 0
                }
        # bencode meta info
        bencoded_info = bencode(info)
        # take SHA-1 hash of this value
        info_hash = hashlib.sha1(bencoded_info).digest()
        # check info_hash_length
        self.assertEqual(len(info_hash), INFO_HASH_LEN)
        # make an announce query
        query = {'info_hash': info_hash,
                 'peer_id': 'BitTorrent-1.0',
                 'ip': '112.113.144.1',
                 'port': '6881'
                 }
        # urlencode this dictionary
        query = urllib.urlencode(query)
        # send GET request to /announce
        response = self.fetch('/announce', 
                            method='GET', 
                            body=query, 
                            follow_redirects=False)
        # if successful, should return 200-OK 
        self.assertEqual(response.code, 200)