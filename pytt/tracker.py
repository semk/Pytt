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
from utils import *


class TrackerStats(tornado.web.RequestHandler):
    """Shows the Tracker statistics on this page.
    """
    def get(self):
        self.send_error(404)


class AnnounceHandler(tornado.web.RequestHandler):
    """Track the torrents. Respond with the peer-list.
    """
    def get(self):
        failure_reason = ''
        warning_message = ''
        # Get all the supported parameters from the HTTP request.
        info_hash = self.get_argument('info_hash')
        peer_id = self.get_argument('peer_id')
        ip = self.get_argument('ip') or self.request.remote_ip
        port = self.get_argument('port')
        uploaded = self.get_argument('uploaded')
        downloaded = self.get_argument('downloaded')
        left = self.get_argument('left')
        compact = self.get_argument('compact')
        no_peer_id = self.get_argument('no_peer_id')
        event = self.get_argument('event')
        numwant = self.get_argument('numwant')
        key = self.get_argument('key')
        trackerid = self.get_argument('trackerid')

        # store the peer info
        store_peer_info(info_hash, peer_id, ip, port)

        # generate response
        response = {}
        # Interval in seconds that the client should wait between sending 
        #    regular requests to the tracker.
        response['interval'] = get_config().get_int('interval')
        # Minimum announce interval. If present clients must not reannounce 
        #    more frequently than this.
        response['min interval'] = get_config().get_int('min_interval')
        response['tracker id'] = tracker_id
        response['complete'] = get_numof_seeders()
        response['incomplete'] = get_numof_leechers()
        response['peers'] = get_peer_list()
        if failure_reason:
            response['failure reason'] = failure_reason
        if warning_message:
            response['warning message'] = warning_message

        # send the bencoded response as text/plain document.
        self.set_header('content-type', 'text/plain')
        self.write(bencode(response))


class ScrapeHandler(tornado.web.RequestHandler):
    """Returns the state of all torrents this tracker is managing.
    """
    def get(self):
        self.send_error(404)


def run_app(port):
    """Start Tornado IOLoop for this application.
    """
    tracker = tornado.web.Application([
        (r"/announce", AnnounceHandler),
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
    parser.add_option('-p', '--port', help='Tracker Port', default=0)
    parser.add_option('-b', '--background', action='store_true', 
                    default=False, help='Start in background')
    parser.add_option('-d', '--debug', action='store_true', 
                    default=False, help='Debug mode')
    (options, args) = parser.parse_args()

    # setup directories
    create_pytt_dirs()

    # set debug option
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        # start the torrent tracker
        run_app(int(options.port) or get_config().get_int('port'))
    except KeyboardInterrupt:
        logging.info('Tracker Stopped.')
        close_db()
        sys.exit(0)
    except Exception, ex:
        logging.fatal('%s' %str(ex))
        close_db()
        sys.exit(-1)


if __name__ == '__main__':
    start_tracker()
