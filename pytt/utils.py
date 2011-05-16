#!/usr/bin/env python
#
# Common utilities for Pytt.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com


import os
import logging
import logging.handlers
import shelve
from socket import inet_aton
from struct import pack
import ConfigParser


CONFIG_PATH = os.path.expanduser('~/.pytt/config/pytt.conf')
DB_PATH = os.path.expanduser('~/.pytt/db/pytt.db')
LOG_PATH = os.path.expanduser('~/.pytt/log/pytt.log')

DEFAULT_ALLOWED_PEERS = 30
MAX_ALLOWED_PEERS = 55

# HTTP Error Codes
MISSING_INFO_HASH = 101
MISSING_PEER_ID = 102
MISSING_PORT = 103


def setup_logging(debug=False):
    """Setup application logging.
    """
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    log_handler = logging.handlers.RotatingFileHandler(LOG_PATH,
                                                      maxBytes=1024*1024,
                                                      backupCount=2)
    root_logger = logging.getLogger('')
    root_logger.setLevel(level)
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format)
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)


def create_config(path):
    """Create default config file.
    """
    logging.info('creating default config at %s' %CONFIG_PATH)
    config = ConfigParser.RawConfigParser()
    config.add_section('tracker')
    config.set('tracker', 'port', '8080')
    config.set('tracker', 'interval', '5')
    config.set('tracker', 'min_interval', '1')
    with open(path, 'wb') as f:
        config.write(f)


def create_pytt_dirs():
    """Create directories to store config, log and db files.
    """
    logging.info('setting up directories for Pytt')
    for path in [CONFIG_PATH, DB_PATH, LOG_PATH]:
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    # create the default config if its not there.
    if not os.path.exists(CONFIG_PATH):
        create_config(CONFIG_PATH)


class ConfigError(Exception):
    """Raised when config error occurs.
    """


class Config:
    """Provide a single entry point to the Configuration.
    """
    __shared_state = {}

    def __init__(self):
        """Borg pattern. All instances will have same state.
        """
        self.__dict__ = self.__shared_state

    def get(self):
        """Get the config object.
        """
        if not hasattr(self, '__config'):
            self.__config = ConfigParser.RawConfigParser()
            if self.__config.read(CONFIG_PATH) == []:
                raise ConfigError('No config at %s' %CONFIG_PATH)
        return self.__config

    def close(self):
        """Close config connection
        """
        if not hasattr(self, '__config'):
            return 0
        del self.__config


class Database:
    """Provide a single entry point to the database.
    """
    __shared_state = {}

    def __init__(self):
        """Borg pattern. All instances will have same state.
        """
        self.__dict__ = self.__shared_state

    def get(self):
        """Get the shelve object.
        """
        if not hasattr(self, '__db'):
            self.__db = shelve.open(DB_PATH, writeback=True)
        return self.__db

    def close(self):
        """Close db connection
        """
        if not hasattr(self, '__db'):
            return 0
        self.__db.close()
        del self.__db


def get_config():
    """Get a connection to the configuration.
    """
    return Config().get()


def get_db():
    """Get a persistent connection to the database.
    """
    return Database().get()


def close_db():
    """Close db connection.
    """
    Database().close()


def no_of_seeders(info_hash):
    """Number of peers with the entire file, aka "seeders".
    """
    db = get_db()
    count = 0
    if db.has_key(info_hash):
        for peer_info in db[info_hash].values():
            if peer_info[3] == 'completed':
                count += 1
    return count


def no_of_leechers(info_hash):
    """Number of non-seeder peers, aka "leechers".
    """
    db = get_db()
    count = 0
    if db.has_key(info_hash):
        for peer_info in db[info_hash].values():
            if peer_info[3] == 'started':
                count += 1
    return count


def store_peer_info(info_hash, peer_id, ip, port, status):
    """Store the information about the peer.
    """
    db = get_db()
    if db.has_key(info_hash):
        if (peer_id, ip, port, status) not in db[info_hash]:
            db[info_hash].append((peer_id, ip, port, status))
    else:
        db[info_hash] = [(peer_id, ip, port, status)]


def get_peer_list(info_hash, numwant, compact, no_peer_id):
    """Get all the peer's info with peer_id, ip and port.
    Eg: [{'peer_id':'#1223&&IJM', 'ip':'162.166.112.2', 'port': '7887'}, ...]
    """
    db = get_db()
    if compact:
        byteswant = numwant * 6
        compact_peers = ""
        # make a compact peer list
        if db.has_key(info_hash):
            for peer_info in db[info_hash]:
                ip = inet_aton(peer_info[1])
                port = pack('>H', int(peer_info[2]))
                compact_peers += (ip+port)
        logging.debug('compact peer list: %r' %compact_peers[:byteswant])
        return compact_peers[:byteswant]
    else:
        peers = []
        if db.has_key(info_hash):
            for peer_info in db[info_hash]:
                p = {}
                p['peer_id'], p['ip'], p['port'], _ = peer_info
                if no_peer_id: del p['peer_id']
                peers.append(p)
        logging.debug('peer list: %r' %peers[:numwant])
        return peers[:numwant]
    
