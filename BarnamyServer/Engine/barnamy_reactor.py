# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from streaming_schema import BarnamyServerSchema
import structlog
import msgpack
import uuid
import datetime
import os
import sys
sys.path.append(os.getcwd() + "/Model")
import Model
import re

logger = structlog.getLogger()
class BarnamyProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.token_id = None
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

    def lineReceived(self, line):
        self.unpacker.feed(line)
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
            else:
                self.sendLine(self.packer.pack(self.schema.error))

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
            self.factory.users[data["nick"]] = self
            message = "%s has joined the channel" % (data["nick"],)

            self.token_id = uuid.uuid1()
            self.broadcastMessage(self.packer.pack({"user_join_left":message, "user_list":self.factory.users.keys(), "user" : self.name}))
            self.sendLine(self.packer.pack({"type":"login", "nick":self.name, "token_id":str(self.token_id), "user_list":self.factory.users.keys()}))
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
        self.factory.users[data["to_"]].sendLine(self.packer.pack(message))

    def handle_FOLDER_SHARE(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        log.msg('Access Folder')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'ACCESS_FOLDER')
        message = {"type":"folder", "from_" : data['from_'], "to_":data['to_']}
        self.factory.users[data["to_"]].sendLine(self.packer.pack(message))

    def handle_FOLDER_SHARE_VALID(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        log.msg('Access Folder Valid')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'ACCESS_FOLDER_VALID')
        message = {"type":"access_folder_valid", "from_" : data['from_'], "to_":data['to_'], 'passwd':data['passwd']}
        self.factory.users[data["to_"]].sendLine(self.packer.pack(message))

    def handle_GET_USER_IP(self, data, log):
        if data["token_id"] != str(self.token_id):
            self.sendLine(self.packer.pack("Where did you get this Token_id :)."))
            return
        log.msg('Get IP')
        bernamylog = Model.barnamydb.Barnamydb()
        bernamylog.save_log(data, data['from_'], 'GET_USER_IP')
        info = {"type":"addr_ip", "from_" : data['from_'], "to_":data['to_']}
        self.factory.users[data["to_"]].sendLine(self.packer.pack(info))

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

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)
    
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

    def kick_user(nick):
        if self.name in self.factory.users:
            del self.factory.users[self.name]

class BarnamyServer(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return BarnamyProtocol(self)
