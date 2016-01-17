# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from os.path import expanduser
BARNAMY_CONF_DIR = expanduser("~/.barnamy")
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'User'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    nick = Column(String(50), nullable=False, unique=True)
    passwd = Column(String(50), nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    date_register = Column(DateTime, nullable=False,  default = datetime.datetime.now)
    active = Column(Boolean, nullable=False,  default = False)

class BernamyLog(Base):
    __tablename__ = 'BernamyLog'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    data = Column(String(250))
    nick = Column(String(250))
    event = Column(String(250), nullable=False)
    date = Column(DateTime,  default = datetime.datetime.now)

class AdminMsg(Base):
    __tablename__ = 'AdminMsg'

    id = Column(Integer, primary_key=True)
    msg = Column(Text)
    nick = Column(String(250))
    date = Column(DateTime,  default = datetime.datetime.now)
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///'+BARNAMY_CONF_DIR+'/barnamydb.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)