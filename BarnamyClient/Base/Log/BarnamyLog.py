# -*- coding: utf-8 -*-

"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

import os
import time
from os.path import expanduser

BARNAMY_LOG_DIR = expanduser("~/.barnamy/Log")

class BarnamyLog(object):

    def __init__(self, Base):
        self.BarnamyBase = Base
        if not os.path.exists(BARNAMY_LOG_DIR):
                os.makedirs(BARNAMY_LOG_DIR)

    def set_log(self, log):
        today = time.strftime("%d_%m_%Y")
        log_f = open("%s/%s-%s.log"%(BARNAMY_LOG_DIR, self.BarnamyBase.nick, today), "a")
        log_f.write(log + "\n")
        log_f.close()

    def set_prv_log(self, log, with_):
        today = time.strftime("%d_%m_%Y")
        log_f = open("%s/%s-%s-%s.log"%(BARNAMY_LOG_DIR, self.BarnamyBase.nick, with_, today), "a")
        log_f.write(log + "\n")
        log_f.close()

    def get_public_log(self):
        pass

    def get_prv_log(self, nick):
        pass
