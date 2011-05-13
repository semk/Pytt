#!/usr/bin/env python
#
# Common utilities for Pytt.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 12th May 2011
# http://foobarnbaz.com


import os
import shelve
import ConfigParser


CONFIG_PATH = os.path.expanduser('~/.pytt/config/pytt.conf')
DB_PATH = os.path.expanduser('~/.pytt/db/pytt.db')
LOG_PATH = os.path.expanduser('~/.pytt/log/pytt.log')


def create_config(path):
    """Create default config file.
    """
    config = ConfigParser.RawConfigParser(path)
    config.set('port', 'int', '8080')
    config.set('interval', 'int', '5')
    config.set('min_interval', 'int', '1')
    with open(path, 'wb') as f:
        config.write(f)


def create_pytt_dirs():
    """Create directories to store config, log and db files.
    """
    for path in [CONFIG_PATH, DB_PATH, LOG_PATH]:
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    # create the default config if its not there.
    if os.path.exists(CONFIG_PATH):
        create_config(CONFIG_PATH)


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
            self.__config.read(CONFIG_PATH)
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


def get_numof_seeders():
    """Number of peers with the entire file, aka "seeders".
    """
    return 0


def get_numof_leechers():
    """Number of non-seeder peers, aka "leechers".
    """
    return 0


def store_peer_info(info_hash, peer_id, ip, port):
    """Store the information about the peer.
    """
    db = get_db()
    if info_hash in db:
        if (peer_id, ip, port) not in db[info_hash]:
            db[info_hash].append((peer_id, ip, port))
    else:
        db[info_hash] = [(peer_id, ip, port)]


def get_peer_list():
    """Get all the peer's info with peer_id, ip and port.
    Eg: [{'peer_id':'#1223&&IJM', 'ip':'162.166.112.2', 'port': '7887'}, ...]
    """
    return []
