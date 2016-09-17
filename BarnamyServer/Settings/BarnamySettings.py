# -*- coding: utf-8 -*-

"""
Created on Sun Apr 24 19:15:14 2016

@author: jamesaxl
"""


import ConfigParser
import os
from os.path import expanduser
BARNAMY_CONF_DIR = expanduser("~/.barnamy")
BARNAMY_CONF_FILE = BARNAMY_CONF_DIR + "/barnamyd.conf"

YES = ["y", "Y", "yes", "YES"]
NO = ["n", "N", "no", "NO", '']

class BarnamySettings(object):
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        if not os.path.isfile(BARNAMY_CONF_FILE):
            pathtls = BARNAMY_CONF_DIR
            database = raw_input("select dabase system (s)qlite | (m)ongodb | ma(r)iadb | (p)ostgresql: ")
            tls = raw_input('Do you want to use TLS (y)es/(n)o default[no] : ')
            while tls not in YES and tls not in NO:
                tls = raw_input('Do you want to use TLS (y)es/(n)o default[no] : ')

            if tls in YES:
                path = raw_input('Set tls path: ')
                while not path and not path.strip():
                    path = raw_input('Set tls path: ')
                pathtls = path 

            while (database not in ['s', 'm', 'r', 'p']):
                database = raw_input("select dabase system (s)qlite | (m)ongodb | ma(r)iadb | (p)ostgresql: ")

            if not os.path.exists(BARNAMY_CONF_DIR):
                os.makedirs(BARNAMY_CONF_DIR)

            self.config.add_section('DataBase')
            if database == 's':
                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'true')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'false')
            elif database == 'm':
                self.config.set('DataBase', 'mongodb', 'true')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'false')
            elif database == 'r':
                db_user = raw_input('Enter database user: ')
                while not db_user or ' ' in db_user:
                    db_user = raw_input('Enter database user: ')

                db_passwd = raw_input('Enter database password: ')
                while not db_passwd or ' ' in db_passwd:
                    db_passwd = raw_input('Enter database password: ')

                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'true')
                self.config.set('DataBase', 'postgresql', 'false')
                self.config.set('DataBase', 'user', db_user)
                self.config.set('DataBase', 'passwd', db_passwd)
            elif database == 'p':
                db_user = raw_input('Enter database user: ')
                while not db_user or ' ' in db_user:
                    db_user = raw_input('Enter database user: ')

                db_passwd = raw_input('Enter database password: ')
                while not db_passwd or ' ' in db_passwd:
                    db_passwd = raw_input('Enter database password: ')

                self.config.set('DataBase', 'mongodb', 'false')
                self.config.set('DataBase', 'sqlite', 'false')
                self.config.set('DataBase', 'mariadb', 'false')
                self.config.set('DataBase', 'postgresql', 'true')
                self.config.set('DataBase', 'user', db_user)
                self.config.set('DataBase', 'passwd', db_passwd)

            self.config.add_section('TLS')
            if tls in YES: self.config.set('TLS', 'stat', 'true')
            else: self.config.set('TLS', 'stat', 'false')

            self.config.set('TLS', 'path', '%s'%pathtls)

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

    def get_info(self):
        self.config.read(BARNAMY_CONF_FILE)
        return (self.config.get('DataBase', 'user'),
                self.config.get('DataBase', 'passwd'))

    def get_tls(self):
        self.config.read(BARNAMY_CONF_FILE)
        if self.config.getboolean('TLS', 'stat'):
            return self.config.get('TLS', 'path')
        else:
            return False
