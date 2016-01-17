# -*- coding: utf-8 -*-
import sys
import os
from bcrypt import hashpw, gensalt
sys.path.append(os.getcwd() + "/Settings")
from Settings.BarnamySettings import BarnamySettings as BRS
from os.path import expanduser
BARNAMY_CONF_DIR = expanduser("~/.barnamy")

session=None
engine = None

DB_ENGINE = BRS()
if DB_ENGINE.get_settings() == "mongodb":
    import barnamyMongoDb
    DB_ENGINE = {'type':'mongodb', 'user':barnamyMongoDb.User, 'log':barnamyMongoDb.BernamyLog, 'admin_msg':barnamyMongoDb.AdminMsg}
elif DB_ENGINE.get_settings() == "sqlite" or DB_ENGINE.get_settings() == "mariadb" or DB_ENGINE.get_settings() == "postgresql":
    from barnamySqliteDb import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.exc import NoResultFound
    if DB_ENGINE.get_settings() == "sqlite":
        import barnamySqliteDb
        engine = create_engine('sqlite:///'+BARNAMY_CONF_DIR+'/barnamydb.db')
        DB_ENGINE = {'type':'sqlite', 'user':barnamySqliteDb.User, 'log':barnamySqliteDb.BernamyLog, 'admin_msg':barnamySqliteDb.AdminMsg}
    elif DB_ENGINE.get_settings() == "mariadb":
        import barnamyMariadb
        engine = create_engine("mysql://root:secret@localhost/barnamydb")
        DB_ENGINE = {'type':'mariadb', 'user':barnamyMariadb.User, 'log':barnamyMariadb.BernamyLog, 'admin_msg':barnamyMariadb.AdminMsg}
    elif DB_ENGINE.get_settings() == "postgresql":
        import barnamyPostgres
        engine = create_engine("postgresql+psycopg2cffi://jamesaxl:secret@localhost/barnamydb")
        DB_ENGINE = {'type':'postgresql', 'user':barnamyPostgres.User, 'log':barnamyPostgres.BernamyLog, 'admin_msg':barnamyPostgres.AdminMsg}

    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

class Barnamydb(object):

    def save_user(self, nick, email, passwd):
        if DB_ENGINE['type'] == 'mongodb':
            user = DB_ENGINE['user'].objects(nick = nick)
            if user:
                return False

            user = DB_ENGINE['user'].objects(email = email)
            if user:
                return False

            user = DB_ENGINE['user']()
            user.nick = nick
            user.email = email
            user.passwd = self.make_hash_password(passwd)
            user.save()
            return True
        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            new_person = DB_ENGINE['user'](nick=nick, email = email, passwd=self.make_hash_password(passwd))
            session.add(new_person)
            session.commit()
            return True

    def save_user_by_admin(self, nick, email, passwd):
        if DB_ENGINE['type'] == 'mongodb':
            user = DB_ENGINE['user'].objects(nick = nick)
            if user:
                return False

            user = DB_ENGINE['user'].objects(email = email)
            if user:
                return False

            user = DB_ENGINE['user']()
            user.nick = nick
            user.email = email
            user.passwd = self.make_hash_password(passwd)
            user.active = True
            user.save()
            return True
        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            new_person = DB_ENGINE['user'](nick=nick, email = email, passwd=self.make_hash_password(passwd), active = True)
            session.add(new_person)
            session.commit()
            return True

    def save_log(self, data, nick, event):
        if DB_ENGINE['type'] == 'mongodb':
            bernamylog = DB_ENGINE['log']()
            bernamylog.data = data
            bernamylog.nick = nick
            bernamylog.event = event
            bernamylog.save()
        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            bernamylog = DB_ENGINE['log'](data=str(data), nick=nick, event=event)
            session.add(bernamylog)
            session.commit()

    def check_dup_user(self, nick):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(nick = nick)
                if user[0].nick: return True
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].nick == nick).one()
                if  user.nick: return True
            except Exception:
                return False

    def check_dup_email(self, email):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(email = email)
                if user[0].email: return True
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].email == email).one()
                if  user.email: return True
            except Exception:
                return False

    def check_user(self, nick, passwd):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(nick = nick)
                if not user[0].active: return False
                return self.check_hash_passwd(user[0].passwd.encode('utf-8'), passwd)
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].nick == nick).one()
                if not user.active: return False
                return self.check_hash_passwd(user.passwd.encode('utf-8'), passwd)
            except Exception:
                return False

    def deactive_user(self, nick):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(nick = nick)
                user.update(**{
                    "set__active": False
                    })
                return True
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].nick == nick).one()
                if  user.nick:
                    user.active = False
                    session.commit()
                    return True
            except Exception:
                return False

    def update_user(self, nick, passwd):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(nick = nick)
                user.update(**{
                    "set__passwd": self.make_hash_password(passwd)
                    })
                return True
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].nick == nick).one()
                if  user.nick:
                    user.passwd = self.make_hash_password(passwd)
                    session.commit()
                    return True
            except Exception:
                return False

    def make_hash_password(self, plain_passwd):
        barnamy_hash = hashpw(plain_passwd, gensalt())
        return barnamy_hash

    def check_hash_passwd(self, hash_passwd, plain_passwd):
        if hashpw(plain_passwd, hash_passwd) == hash_passwd:
            return True
        else:
            return False

    def get_requests(self):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(active = False)
                return user
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].active == False)
                return user
            except Exception:
                return False

    def allow_user(self, nick):
        if DB_ENGINE['type'] == 'mongodb':
            try:
                user = DB_ENGINE['user'].objects(nick = nick)
                user.update(**{
                "set__active": True
                    })                
            except Exception:
                return False

        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            try:
                user = session.query(DB_ENGINE['user']).filter(DB_ENGINE['user'].nick == nick).one()
                if  user.nick:
                    user.active = True
                    session.commit()
            except Exception:
                return False

    def save_user_msg_to_admin(self, nick, msg):
        if DB_ENGINE['type'] == 'mongodb':
            request = DB_ENGINE['admin_msg']()
            request.nick = nick
            request.msg = msg
            request.save()
        elif DB_ENGINE['type'] == 'sqlite' or DB_ENGINE['type'] == 'mariadb' or DB_ENGINE['type'] == 'postgresql':
            request = DB_ENGINE['adminmsg'](nick = nick, msg = msg)
            request.commit()
