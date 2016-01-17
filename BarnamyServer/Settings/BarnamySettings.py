# -*- coding: utf-8 -*-

import ConfigParser
import os
from os.path import expanduser
BARNAMY_CONF_DIR = expanduser("~/.barnamy")
BARNAMY_CONF_FILE = BARNAMY_CONF_DIR + "/barnamyd.conf"

class BarnamySettings(object):
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        if not os.path.isfile(BARNAMY_CONF_FILE):
            pathtls = BARNAMY_CONF_DIR
            database = raw_input('Please chose database engine [sqlite, mongodb, mariadb, postgresql]: ')
            tls = raw_input('Do you want to use TLS: ')
            if tls == 'y' or tls == 'Y':
                path = raw_input('Set tls path: ')
                if path: pathtls = path 
                
            while (database not in ['sqlite', 'mongodb', 'mariadb', 'postgresql']):
                database = raw_input('Please chose database engine [sqlite, mongodb, mariadb, postgresql]')

            if not os.path.exists(BARNAMY_CONF_DIR):
                os.makedirs(BARNAMY_CONF_DIR)

            self.config.add_section('DataBase')
            if database == 'sqlite':
                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'true')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'false')
            elif database == 'mongodb':
                self.config.set('DataBase', 'mongodb', 'true')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'false')
            elif database == 'mariadb':
                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'true')
                self.config.set('DataBase', 'postgresql', 'false')
            elif database == 'postgresql':
                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'true')

            self.config.add_section('TLS')
            if tls == 'y': self.config.set('TLS', 'stat', 'true')
            else: self.config.set('TLS', 'stat', 'false')

            self.config.set('TLS', 'path', '%s'%pathtls)

            # Writing our configuration file to 'example.cfg'
            with open(BARNAMY_CONF_FILE, 'wb') as configfile:
                self.config.write(configfile)

    def get_settings(self):
        self.config.read(BARNAMY_CONF_FILE)
        if self.config.getboolean('DataBase', 'mongodb'):
            return "mongodb"
        elif self.config.getboolean('DataBase', 'sqlite'):
            return "sqlite"
        elif self.config.getboolean('DataBase', 'mariadb'):
            return "mariadb"
        elif self.config.getboolean('DataBase', 'postgresql'):
            return "postgresql"

    def get_tls(self):
        self.config.read(BARNAMY_CONF_FILE)
        if self.config.getboolean('TLS', 'stat'):
            return self.config.get('TLS', 'path')
        else:
            return False
