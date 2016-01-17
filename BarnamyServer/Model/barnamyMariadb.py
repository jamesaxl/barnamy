# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    nick = Column(String(50), nullable=False, unique=True)
    passwd = Column(Text, nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    date_register = Column(DateTime, nullable=False,  default = datetime.datetime.now)
    active = Column(Boolean, nullable=False,  default = False)

class BernamyLog(Base):
    __tablename__ = 'BernamyLog'

    id = Column(Integer, primary_key=True)
    data = Column(Text)
    nick = Column(String(250))
    event = Column(String(250), nullable=False)
    date = Column(DateTime,  default = datetime.datetime.now)
 
class AdminMsg(Base):
    __tablename__ = 'AdminMsg'

    id = Column(Integer, primary_key=True)
    msg = Column(Text)
    nick = Column(String(50))
    date = Column(DateTime,  default = datetime.datetime.now)

engine = create_engine("mysql://root:secret@localhost/barnamydb")
 
Base.metadata.create_all(engine)