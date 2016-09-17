# -*- coding: utf-8 -*-

"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

from mongoengine import *
import datetime
connect('barnamydb')

class User(Document):

    nick = StringField(max_length=20, required=True, unique=True)
    passwd = StringField(required=True)
    email = StringField(max_length=30, required=True, unique=True)
    date_register = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default = False)

class BernamyLog(Document):
    
    data = DictField(required=True)
    nick = StringField(required=True)
    event = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now)

class AdminMsg(Document):
    
    msg = StringField(required=True)
    nick = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now)
