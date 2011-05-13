#!/usr/bin/env python
#
# BitTorrent Tracker using Tornado
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com

import logging
import tornado.ioloop
import tornado.web
from bencode import bencode, bdecode

class TrackerStats(tornado.web.RequestHandler):
    """Shows the Tracker statistics on this page.
    """
    def get(self):
        self.send_error(404)

class AnnounceHandler(tornado.web.RequestHandler):
    """Track the torrents. Respond with the peer-list.
    """
    def get(self):
        # Get all the supported parameters from the HTTP request.
        info_hash = self.get_argument('info_hash')
        peer_id = self.get_argument('peer_id')
        port = self.get_argument('port')
        uploaded = self.get_argument('uploaded')
        downloaded = self.get_argument('downloaded')
        left = self.get_argument('left')
        compact = self.get_argument('compact')
        no_peer_id = self.get_argument('no_peer_id')
        event = self.get_argument('event')
        ip = self.get_argument('ip') or self.request.remote_ip
        numwant = self.get_argument('numwant')
        key = self.get_argument('key')
        trackerid = self.get_argument('trackerid')

class ScrapeHandler(tornado.web.RequestHandler):
    """Returns the state of all torrents this tracker is managing.
    """
    def get(self):
        self.send_error(404)

tracker = tornado.web.Application([
    (r"/announce",AnnounceHandler),
    (r"/scrape", ScrapeHandler),
    (r"/", TrackerStats),
])

if __name__ == "__main__":
    tracker.listen(8888)
    tornado.ioloop.IOLoop.instance().start()