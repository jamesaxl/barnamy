# -*- coding: utf-8 -*-

"""
Created on Sun Apr 24 19:15:14 2016

@author: jamesaxl
"""

from schema import Schema, And, Use

class  BarnamyClientSchema(object):
    
    def __init__(self):
        self.status_ok_schema = Schema({'status' :And(str)})
        
        self.error = {"login_syntax" : '{"type":"login", "nick":"4 <= len(str) <= 10", "passwd":"str"}',
                      "register_syntax" : '{"type":"register", "nick":"4 <= len(str) <= 10", "passwd":"str", "email":"str"}',
                      "pub_public_msg_syntax" : '{"type":"public", "nick":"4 <= len(str) <= 10", "token_id":"str", "msg":"str"}',
                      "pub_public_msg_syntax" : '{"type":"public", "nick":"4 <= len(str) <= 10", "token_id":"str", "msg":"str"}'}

        self.user_join_left_schema = Schema({'user_join_left' :And(str), 'user_list': And(list), 'user' :And(str)})
        
        self.login_ok_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'login'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str), 'user_list': And(list)})
        self.login_nok_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'err_login'),
                                       'msg': And(str)})
        
        self.check_token_id_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'check_token_id'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'token_id':And(str)})
        
        self.register_ok_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'register'),
                                       'succ':And(str)})
        self.msg_ok_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'public'),
                                       'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'msg':And(str)})
        self.prv_msg_ok_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'private'),
                                       'to_':And(str), 'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'msg':And(str)})
        
        self.access_folder_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'folder'),
                                       'to_':And(str), 'from_': And(str)})
        
        self.status_ = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'status'),
                                       'status':And(str), 'nick': And(str)})

        self.access_folder_valid = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'access_folder_valid'),
                                       'from_': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'to_':And(str), 'passwd':And(str)})
    
        self.info_user = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'info'),
                                       'nick': And(str, Use(str.lower), lambda n: 4 <= len(n) <= 10),
                                       'info':And(str)})
        
        self.kick_schema = Schema({'type' : And(str, Use(str.lower), lambda n: n == 'kick'),
                                       'msg': And(str)})
    def status_schema_f(self, data):
        try:
            data = self.status_ok_schema.validate(data)
            return True
        except Exception:
            return False

    def check_token_id_schema_f(self, data):
        try:
            data = self.check_token_id_schema.validate(data)
            return True
        except Exception:
            return False

    def kick_schema_user_f(self, data):
        try:
            data = self.kick_schema.validate(data)
            return True
        except Exception:
            return False

    def status_schema_user_f(self, data):
        try:
            data = self.status_.validate(data)
            return True
        except Exception:
            return False

    def info_user_schema_user_f(self, data):
        try:
            data = self.info_user.validate(data)
            return True
        except Exception:
            return False
    

    def login_nok_schema_f(self, data):
        try:
            data = self.login_nok_schema.validate(data)
            return True
        except Exception:
            return False

    def access_folder_schema_f(self, data):
        try:
            data = self.access_folder_schema.validate(data)
            return True
        except Exception:
            return False

    def access_folder_valid_schema_f(self, data):
        try:
            data = self.access_folder_valid.validate(data)
            return True
        except Exception:
            return False

    def error_schema_f(self, data):
        if self.error == data:
            return True
        return False

    def user_join_left_schema_f(self, data):
        try:
            data = self.user_join_left_schema.validate(data)
            return True
        except Exception:
            return False


    def login_schema_f(self, data):
        try:
            data = self.login_ok_schema.validate(data)
            return True
        except Exception:
            return False
    
    def register_schema_f(self, data):
        try:
            data = self.register_ok_schema.validate(data)
            return True
        except Exception:
            return False
    
    def public_message_f(self, data):
        try:
            data = self.msg_ok_schema.validate(data)
            return True
        except Exception:
            return False
    
    def private_message_f(self, data):
        try:
            data = self.prv_msg_ok_schema.validate(data)
            return True
        except Exception:
            return False