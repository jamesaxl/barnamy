# -*- coding: utf-8 -*-

"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    nick = Column(String(20), nullable=False, unique=True)
    passwd = Column(Text, nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    date_register = Column(DateTime, nullable=False,  default = datetime.datetime.now)
    active = Column(Boolean, nullable=False,  default = False)

class BernamyLog(Base):
    __tablename__ = 'BernamyLog'

    id = Column(Integer, primary_key=True)
    data = Column(Text)
    nick = Column(String(20))
    event = Column(Text, nullable=False)
    date = Column(DateTime,  default = datetime.datetime.now)

class AdminMsg(Base):
    __tablename__ = 'AdminMsg'

    id = Column(Integer, primary_key=True)
    msg = Column(Text)
    nick = Column(String(20))
    date = Column(DateTime,  default = datetime.datetime.now)
