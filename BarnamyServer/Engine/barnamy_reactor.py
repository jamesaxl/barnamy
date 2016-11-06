# -*- coding: utf-8 -*-

"""
Created on Sun Apr 24 19:15:14 2016

@author: jamesaxl
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.web import resource
from streaming_schema import BarnamyServerSchema
import structlog
import json
import msgpack
import uuid
import datetime
import os
import sys
sys.path.append(os.getcwd() + "/Model")
import Model
import re
import random

logger = structlog.getLogger()
class BarnamyProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.token_id = None
        self.allow_sync_server = {}
        self.unpacker = msgpack.Unpacker()
        self.packer = msgpack.Packer()
        self.schema = BarnamyServerSchema()

    def connectionMade(self):
        self.sendLine(self.packer.pack({"status":"connected: Welcome to Barnamy"}))
        self._log = logger.new(
            connection_id=str(uuid.uuid4()),
            peer=self.transport.getPeer().host,
            date_time=datetime.datetime.utcnow(),
        )

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.token_id = None
            message = "%s has left the channel" % (self.name,)
            data = {"user_join_left" : message, "user_list" : self.factory.users.keys(), "user" : self.name}
            self.broadcastMessage(self.packer.pack(data))
            log = self._log.bind(data=data)
            log.msg(message)

    def lineReceived(self, data):
        self.unpacker.feed(data)
        data = self.unpacker.unpack()
        log = self._log.bind(data=data)
        if self.token_id == None:
            if self.schema.login_schema_f(data):
                self.handle_LOGIN(data, log)
            elif self.schema.register_schema_f(data) :
                self.handle_REGISTER( data, log)
            else:
                self.sendLine(self.packer.pack(self.schema.error))
        else:
            if self.schema.public_message_f(data):
                self.handle_CHAT(data, log)
            elif self.schema.private_message_f(data):
                self.handle_PRVCHAT(data, log)
            elif self.schema.logout_f(data):
                self.logout(data, log)
            elif self.schema.access_folder_f(data):
                self.handle_FOLDER_SHARE(data, log)
            elif self.schema.status_f(data):
                self.handle_STATUS(data, log)
            elif self.schema.msg_admin_f(data):
                self.handle_ADMINMSG(data, log)
            elif self.schema.access_folder_valid_f(data):
                self.handle_FOLDER_SHARE_VALID(data, log)
            elif self.schema.ignore_user_f(data):
                self.handle_IGNORE_USER(data, log)
            elif self.schema.unignore_user_f(data):
                self.handle_UNIGNORE_USER(data, log)
            elif self.schema.info_user_f(data):
                self.handle_INFO_USER(data, log)
            elif self.schema.kick_user_f(data):
                self.handle_KICK_USER(data, log)
            elif self.schema.sync_between_srv_f(data):
                pass
            else:
                self.sendLine(self.packer.pack(self.schema.error))

    def handle_SYNC_SRV(self, data, log):
        if not data['addr'] in self.allow_sync_server:
            return

    def handle_REGISTER(self, data, log):
        if data['nick'] and data['email'] and ['passwd']:
            user = Model.barnamydb.Barnamydb()
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", data['email']) == None:
                self.sendLine(self.packer.pack(self.schema.error))
                return
            if re.match("^[a-z]+[_]*[a-z]*$", data['nick']) == None:
                self.sendLine(self.packer.pack(self.schema.error))
                return

            if not user.save_user(data['nick'], data['email'],data['passwd']):
                self.sendLine(self.packer.pack({"msg":"Nick is already choosen."}))
                return

            bernamylog = Model.barnamydb.Barnamydb()
            bernamylog.save_log(data, data['nick'], 'REGISTER')
            log.msg('REGISTER')
            self.sendLine(self.packer.pack({"succ":"User is registered", "type":"register"}))
        else:
            self.sendLine(self.packer.pack(self.schema.error))

    def handle_STATUS(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        data = {'type': 'status', 'nick': data['nick'], 'status':data['status']}
        self.broadcastMessage(self.packer.pack(data))
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['nick'], 'STATUS')
        log.msg('STATUS')

    def handle_LOGIN(self, data, log):
        if data["nick"] in self.factory.users:
            self.sendLine(self.packer.pack("you are already logged in."))
            return
        user = Model.barnamydb.Barnamydb()
        if user.check_user(data['nick'], data['passwd']):
            self.name = data["nick"]
            self.factory.ignore_users[self.name] = []
            self.factory.users[data["nick"]] = [self, self.transport.getPeer().host]
            message = "%s has joined the channel" % (self.name,)

            self.token_id = uuid.uuid1()
            self.broadcastMessage(self.packer.pack({"user_join_left":message, "user_list":self.factory.users.keys(), 
                                                    "user" : self.name}))
            self.sendLine(self.packer.pack({"type":"login", "nick":self.name, "token_id":str(self.token_id), 
                                            "user_list":self.factory.users.keys()}))
            log.msg('LOGIN')
            bernamylog = Model.barnamydb.Barnamydb()
            bernamylog.save_log(data, data['nick'], 'LOGIN')
        else:
            self.sendLine(self.packer.pack({"type":"err_login", "msg":"check nick and password"}))

    def handle_CHAT(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return

        log.msg('PUBLIC MSG')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['nick'], 'PUBLIC_MSG')
        data = {"type":"public", "from_":data['nick'], "msg":data['msg']}
        self.broadcastMessage(self.packer.pack(data))
    
    def handle_PRVCHAT(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        log.msg('PRIVATE MSG')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'PRIVATE_MSG')
        message = {"type":"private", "from_" : data['from_'], "to_":data['to_'], "msg":data['msg']}
        if not data['to_'] in self.factory.ignore_users[self.name]:
            if not self.name in self.factory.ignore_users[data['to_']]:
                self.factory.users[data["to_"]][0].sendLine(self.packer.pack(message))

    def handle_FOLDER_SHARE(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        if data['from_'] in self.factory.ignore_users[self.name]:
            return
        log.msg('Access Folder')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'ACCESS_FOLDER')
        message = {"type":"folder", "from_" : data['from_'], "to_":data['to_']}
        self.factory.users[data["to_"]][0].sendLine(self.packer.pack(message))

    def handle_FOLDER_SHARE_VALID(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        log.msg('Access Folder Valid')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'ACCESS_FOLDER_VALID')
        message = {"type":"access_folder_valid", "from_" : data['from_'], "to_":data['to_'], 'passwd':data['passwd']}
        self.factory.users[data["to_"]][0].sendLine(self.packer.pack(message))

    def handle_ADMINMSG(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return

        if data['msg'].split(' ')[0] == "/admin" and data['msg'].split(' ')[1]:

            log.msg('Admin msg')
            bernamylog = Model.barnamydb.Barnamydb()
            bernamylog.save_log(data, data['nick'], 'ADMIN_MSG')
            barnamy_admin_msg = Model.barnamydb.Barnamydb()
            barnamy_admin_msg.save_user_msg_to_admin(data['nick'], data['msg'])

    def handle_IGNORE_USER(self, data, log):
        if data['nick'] == self.name:
            return

        self.factory.ignore_users[self.name].append(data['nick'])
        log.msg('Ignore user')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['nick'], 'IGNORE')

    def handle_UNIGNORE_USER(self, data, log):
        if data['nick'] == self.name:
            return

        self.factory.ignore_users[self.name].remove(data['nick'])
        log.msg('Unignore user')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['nick'], 'UNIGNORE')

    def handle_INFO_USER(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return

        data = {"type":"info", "nick" : data['nick'], "info": self.factory.users[data["nick"]][1]}
        self.factory.users[self.name][0].sendLine(self.packer.pack(data))
        log.msg('Info user')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['nick'], 'INFO')

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if not name in self.factory.ignore_users[self.name]:
                if not self.name in self.factory.ignore_users[name]:
                    if protocol[0] != self:
                        protocol[0].sendLine(message)

    def logout(self, data, log):
        log.msg('LOGOUT')
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        if self.name in self.factory.users:
            del self.factory.users[self.name]
        self.token_id = None
        message = "%s has left the channel" % (self.name,)
        data = {"user_join_left" : message, "user_list" : self.factory.users.keys(), "user" : self.name}
        self.broadcastMessage(self.packer.pack(data))
        log = self._log.bind(data=data)
        log.msg(message)

    # It does not work as we want
    def handle_KICK_USER(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        from_ = data["from_"]
        nick = data["nick"]
        if nick != from_:
            if nick in self.factory.users:
                user = Model.barnamydb.Barnamydb()
                if user.check_admin(from_):
                    del self.factory.users[nick]
                    message = "%s kicked by %s" % (nick, from_)
                    data = {"type" : "kick", "msg" : message}
                    self.sendLine(self.packer.pack(data))
                    log = self._log.bind(data=data)
                    log.msg(message)
                else:
                    message = "You are not admin"
                    data = {"type" : "kick", "msg" : message}
                    self.factory.users[from_][0].sendLine(self.packer.pack(data))
        else:
            message = "You can not kick yourself from channel"
            data = {"type" : "kick", "msg" : message}
            self.factory.users[from_][0].sendLine(self.packer.pack(data))

class BarnamyServer(Factory):

    def __init__(self):
        self.users = {}
        self.ignore_users = {}

    def buildProtocol(self, addr):
        return BarnamyProtocol(self)

    class ServerQuotes(resource.Resource):
        isLeaf = True
        QUOTES = None

        def render_POST(self, request):
            return 'DONE'

        def render_GET(self, request):
            with open(os.getcwd() + '/Engine/quotes.json') as data_file:
                self.QUOTES = json.load(data_file) 
            key = random.choice(self.QUOTES.keys())
            index = random.randint(0, len(self.QUOTES[key]) - 1)
            return json.dumps({key : self.QUOTES[key][index]})
            

        def render_PUT(self, request):
            return "Put"

        def render_DELETE(self, request):
            return "Delete"

