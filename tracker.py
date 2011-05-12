#!/usr/bin/env python
#
# BitTorrent Tracker using Tornado
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class AnnounceHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class ScrapeHandler(tornado.web.RequestHandler):
    def get(self):
        pass

tracker = tornado.web.Application([
    (r"/announce",AnnounceHandler),
    (r"/scrape", ScrapeHandler),
    (r"/", MainHandler),
])

if __name__ == "__main__":
    tracker.listen(8888)
    tornado.ioloop.IOLoop.instance().start()