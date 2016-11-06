# -*- coding: utf-8 -*-

"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

from schema import Schema, And, Use

class BarnamyServerSchema(object):
    
    def __init__(self):
        self.login_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'login'),
                                       'nick': And(str),
                                       'passwd':And(str)})
        self.register_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'register'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'passwd':And(str, lambda n: 7 <= len(n) ), 'email':And(str, Use(str.lower))})
        self.msg_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'public'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str), 'msg':And(str)})
        self.prv_msg_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'private'),
                                       'to_':And(str), 'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str), 'msg':And(str)})

        self.logout_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'logout'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str)})

        self.access_folder_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'folder'),
                                       'to_':And(str), 'from_': And(str),
                                       'token_id':And(str)})

        self.status_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'status'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str), 'status':And(str)})

        self.msg_admin = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'admin'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str), 'msg':And(str)})

        self.access_folder_valid = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'access_folder_valid'),
                                       'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'to_':And(str), 'passwd':And(str, lambda n: 7 <= len(n) ), 'token_id':And(str)})
        self.ignore_user = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'ignore'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str)})

        self.unignore_user = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'unignore'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str)})

        self.info_user = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'info'),
                                       'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str)})

        self.kick_user = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'kick'),
                                       'from_' : And(str, Use(str)), 'nick': And(str, Use(str)), 
                                       'token_id' : And(str)})

        self.sync_between_srv = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'sync'),
                                       'addr': And(str),
                                       'port' : And(str),
                                       'users': And(list),
                                       'ignore_users':And(str)})

        self.error = {"login_syntax" : '{"type":"login", "nick":"4 <= len(str) <= 10", "passwd":"str"}',
                      "register_syntax" : '{"type":"register", "nick":"4 <= len(str) <= 10", "passwd":"str", "email":"str"}',
                      "pub_public_msg_syntax" : '{"type":"public", "nick":"4 <= len(str) <= 10", "token_id":"str", "msg":"str"}',
                      "pub_public_msg_syntax" : '{"type":"public", "nick":"4 <= len(str) <= 10", "token_id":"str", "msg":"str"}'}
    
    def sync_between_srv_f(self, data):
        try:
            data = self.sync_between_srv.validate(data)
            return True
        except Exception:
            return False

    def kick_user_f(self, data):
        try:
            data = self.kick_user.validate(data)
            return True
        except Exception:
            return False

    def login_schema_f(self, data):
        try:
            data = self.login_schema.validate(data)
            return True
        except Exception:
            return False

    def ignore_user_f(self, data):
        try:
            data = self.ignore_user.validate(data)
            return True
        except Exception:
            return False

    def unignore_user_f(self, data):
        try:
            data = self.unignore_user.validate(data)
            return True
        except Exception:
            return False

    def info_user_f(self, data):
        try:
            data = self.info_user.validate(data)
            return True
        except Exception:
            return False

    def msg_admin_f(self, data):
        try:
            data = self.msg_admin.validate(data)
            return True
        except Exception:
            return False

    def access_folder_valid_f(self, data):
        try:
            data = self.access_folder_valid.validate(data)
            return True
        except Exception:
            return False

    def access_folder_f(self, data):
        try:
            data = self.access_folder_schema.validate(data)
            return True
        except Exception:
            return False
    
    def status_f(self, data):
        try:
            data = self.status_schema.validate(data)
            return True
        except Exception:
            return False   
    
    def register_schema_f(self, data):
        try:
            data = self.register_schema.validate(data)
            return True
        except Exception:
            return False
    
    def public_message_f(self, data):
        try:
            data = self.msg_schema.validate(data)
            return True
        except Exception:
            return False
    
    def private_message_f(self, data):
        try:
            data = self.prv_msg_schema.validate(data)
            return True
        except Exception:
            return False

    def logout_f(self, data):
        try:
            data = self.logout_schema.validate(data)
            return True
        except Exception:
            return False
