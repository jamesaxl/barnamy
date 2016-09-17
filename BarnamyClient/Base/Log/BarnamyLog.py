# -*- coding: utf-8 -*-

"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

import os
from os.path import expanduser

BARNAMY_LOG_DIR = expanduser("~/.barnamy/Log")
class BarnamyLog(object):

    def __init__(self):
        if not os.path.exists(BARNAMY_LOG_DIR):
                os.makedirs(BARNAMY_LOG_DIR)

    def set_log(self, log_type, log):
        log_f = open("%s/%s.log"%(BARNAMY_LOG_DIR, log_type), "a")
        log_f.write(log + "\n")
        log_f.close()

    def get_log(self, log_type, nick = 0):
        pass
