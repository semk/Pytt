#!/usr/bin/env python
#
# BitTorrent Tracker using Tornado
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com


import sys
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from optparse import OptionParser
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


def run_app(port):
    """Start Tornado IOLoop for this application.
    """
    tracker = tornado.web.Application([
        (r"/announce",AnnounceHandler),
        (r"/scrape", ScrapeHandler),
        (r"/", TrackerStats),
    ])
    logging.info('Starting Pytt on port %d' %port)
    http_server = tornado.httpserver.HTTPServer(tracker)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


def start_tracker():
    """Start the Torrent Tracker.
    """
    # parse commandline options
    parser = OptionParser()
    parser.add_option('-p', '--port', help='Tracker Port', default=8080)
    parser.add_option('-b', '--background', action='store_true', 
                    default=False, help='Start in background')
    parser.add_option('-d', '--debug', action='store_true', 
                    default=False, help='Debug mode')
    (options, args) = parser.parse_args()

    # set debug option
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
    	logging.basicConfig(level=logging.INFO)

    try:
        # start the torrent tracker
        run_app(int(options.port))
    except KeyboardInterrupt:
        logging.info('Tracker Stopped.')
    except Exception, ex:
        logging.fatal('%s' %str(ex))
        sys.exit(-1)


if __name__ == '__main__':
    start_tracker()
