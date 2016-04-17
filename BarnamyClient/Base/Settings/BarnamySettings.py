# -*- coding: utf-8 -*-

import ConfigParser
import os
from os.path import expanduser
BARNAMY_CONF_DIR = expanduser("~/.barnamy")
BARNAMY_CONF_FILE = BARNAMY_CONF_DIR + "/barnamyc.conf"

class BarnamySettings(object):
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        if not os.path.isfile(BARNAMY_CONF_FILE):
            if not os.path.exists(BARNAMY_CONF_DIR):
                os.makedirs(BARNAMY_CONF_DIR)

            self.config.add_section('BASE')
            self.config.set('BASE', 'URL/IP', '127.0.0.1')
            self.config.set('BASE', 'Port', '60251')
            self.config.set('BASE', 'WPort', '8080')
            self.config.set('BASE', 'Sound', 'false')
            self.config.set('BASE', 'Notify', 'false')
            self.config.set('BASE', 'Log', 'false')
            self.config.set('BASE', 'Tls', 'false')

            with open(BARNAMY_CONF_FILE, 'wb') as configfile:
                self.config.write(configfile)

    def get_settings(self):
        settings = {}
        self.config.read(BARNAMY_CONF_FILE)
        settings['ip'] = self.config.get('BASE', "URL/IP")
        settings['port'] = self.config.getint('BASE', 'Port')
        settings['wport'] = self.config.getint('BASE', 'WPort')
        settings['sound'] = self.config.getboolean('BASE', 'Sound')
        settings['notify'] =  self.config.getboolean('BASE', 'Notify')
        settings['log'] =  self.config.getboolean('BASE', 'Log')
        settings['tls'] =  self.config.getboolean('BASE', 'Tls')
        return settings

    def save_settings(self, settings):
        #self.config.add_section('BASE')
        self.config.set('BASE', 'URL/IP', settings['ip'])
        self.config.set('BASE', 'Port', settings['port'])
        self.config.set('BASE', 'WPort', settings['wport'])
        self.config.set('BASE', 'Sound', settings['sound'])
        self.config.set('BASE', 'Notify', settings['notify'])
        self.config.set('BASE', 'Log', settings['log'])
        self.config.set('BASE', 'Tls', settings['tls'])

        with open(BARNAMY_CONF_FILE, 'wb') as configfile:
            self.config.write(configfile)