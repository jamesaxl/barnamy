# -*- coding: utf-8 -*-

"""
Created on Sun Apr 24 19:15:14 2016

@author: jamesaxl
"""

from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from streaming_schema import BarnamyClientSchema
from Settings.BarnamySettings import BarnamySettings as BRS
from PasteBin.barnamyPasteBin import BarnamayPastBin as BRP
from Log.BarnamyLog import BarnamyLog as BRL
from time import strftime
import subprocess
import msgpack
import GUI
import Audio
import Notify
import os
import signal
import getpass
from os.path import expanduser
import random
import string
import json
import urllib2
from twisted.internet import reactor
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

BARNAMY_HOME = expanduser("~/BarnamyHome")
BARNAMY_HTTP_PASSWD_FILE = expanduser("~/.barnamy/httpd.password")
BARNAMY_MINI_WEB_SRV_PID = "/tmp/barnamyminisrv.pid"
USER = getpass.getuser()

class BarnamyClient(LineReceiver):

    def connectionMade(self):
        self.packer = msgpack.Packer()
        self.unpacker = msgpack.Unpacker()
        self.schema = BarnamyClientSchema()
        self.barnamy_setting_i = BRS()
        self.token_id = None
        self.nick = None
        self._pid = None
        self.msg_sent_list = []
        self.msg_sent_position = None
        
        self.barnamy_cmd = {'/admin' : 'for sending message to Admin e.g /admin <msg>', 
        '/ignore' : 'to ignore user e.g /ignore <nick>',
        '/unignore' : 'to unignore user e.g /unignore <nick>', '/run_srv':'Run barnamy server', 
        '/stop_srv':'Stop barnamy server', '/allow' : 'to allow user join private folder e.g /allow <nick>', 
        '/away' : 'Become away', '/online' : 'Become online', '/info' : 'get user info e.g /info nick', 
        '/quote' : 'print a quote',  '/flkg' : 'Play False king theme', '/stop_flkg' : 'Stop False king theme',
        '/pastebin' : 'Open pastebin Layout', 
        '/prvmsg' : 'send private message to a user/users eg: /prvmsg {delay on second} {nick:msg} => /prvmsg 3 jamesaxl:hello Mr.,falseking:to hell Blind Man'}

        self.barnamy_settings_actions = {'save_settings' : self.save_settings, 
                                         'get_settings' : self.get_settings}

        self.barnamy_sound_setting = {'send_prv_msg_sound' : self.send_prv_msg_sound, 'login_sound' : self.login_sound,
         'logout_sound' : self.logout_sound, 'received_prv_msg_sound' : self.received_prv_msg_sound, 
         'access_folder_sound' : self.access_folder_sound, 'play_false_king_theme' : self.play_false_king_theme, 
         'stop_false_king_theme' : self.stop_false_king_theme}

        self.barnamy_actions = {'send_pub_msg' : self.send_pub_msg, 'send_prv_msg' : self.send_prv_msg, 
                                'do_login': self.do_login, 'do_logout' : self.do_logout, 
                                'ask_for_folder_access' : self.ask_for_folder_access,
                                'regiser_new_user' : self.regiser_new_user,'_notify' : self._notify, 
                                '_log' : self._log, '_prv_log' : self._prv_log, 
                                'start_web_server' : self.start_web_server,
                                'stop_web_server':self.stop_web_server, 'accept_share' : self.accept_share, 
                                'ignore_user': self.ignore_user, 'unignore_user': self.unignore_user, 
                                'get_info' : self.get_info, 'call_quote' : self.call_quote,
                                'kick_user' : self.kick_user, 'paste_bin' : self.paste_bin,
                                'prv_msg_cmd' : self.prv_msg_cmd}

        self.barnamy_status = {'online' : self.go_online, 'away' : self.go_away}
        
        self.BarnamyPlayer = Audio.BarnamyAudio.BarnamyAudio()
        self.BarnamyNotify = Notify.BarnamyNotify.BarnamyNotify()
        self.app = GUI.BarnamyLogin.BarnamyLogin(self)
        self.barnamy_log = BRL(self)
        self.app.RunBarnamyLogin()

    def connectionLost(self, reason):
        context_id = self.app.statusbar.get_context_id("barnamy")
        message_id = self.app.statusbar.push(context_id, "connection lost: verifier your settings")


    def regiser_new_user(self, data):
        self.sendLine(self.packer.pack(data))

    def do_login(self, data):
        self.sendLine(self.packer.pack(data))

    def do_logout(self, data):
        self.sendLine(self.packer.pack(data))
        self.barnamy_sound_setting['logout_sound']()
        self.nick = None
        self.token_id = None

    def ask_for_folder_access(self, data):
        self.sendLine(self.packer.pack(data))

    def send_pub_msg(self, data):
        self.barnamy_actions['_log'](data)
        self.sendLine(self.packer.pack(data))

    def login_sound(self):
        if self.barnamy_setting_i.get_settings()['sound']:
            self.BarnamyPlayer.login_sound()

    def received_prv_msg_sound(self):
        if self.barnamy_setting_i.get_settings()['sound']:
            self.BarnamyPlayer.receive_msg_sound()

    def logout_sound(self):
        if self.barnamy_setting_i.get_settings()['sound']:
            self.BarnamyPlayer.logout_sound()

    def access_folder_sound(self):
        if self.barnamy_setting_i.get_settings()['sound']:
            self.BarnamyPlayer.access_folder_sound()

    def go_online(self, data):
        self.sendLine(self.packer.pack(data))

    def go_away(self, data):
        self.sendLine(self.packer.pack(data))

    def send_prv_msg(self, data):
        self.barnamy_actions['_prv_log'](data)
        self.barnamy_sound_setting['send_prv_msg_sound']()
        self.sendLine(self.packer.pack(data))

    def prv_msg_cmd(self, delay, data):
        reactor.callLater(float(delay), self.send_prv_msg, data)

    def send_prv_msg_sound(self):
        if self.barnamy_setting_i.get_settings()['sound']:
            self.BarnamyPlayer.send_msg_sound()

    def send_paste_bin(self, data):
        self.sendLine(self.packer.pack(data))

    def _notify(self, data1, data2):
        if self.barnamy_setting_i.get_settings()['notify']:
            self.BarnamyNotify.show_notify(data1, data2)

    def save_settings(self, data):
        self.barnamy_setting_i.save_settings(data)

    def get_settings(self):
        settings = self.barnamy_setting_i.get_settings()
        return settings

    def _log(self, data):
        if self.barnamy_setting_i.get_settings()['log']:
            log = "[%s] <%s> %s" %(strftime("%H:%M:%S"), data['nick'], data['msg'])
            self.barnamy_log.set_log(log)

    def _prv_log(self, data):
        if self.barnamy_setting_i.get_settings()['log']:
            with_ = data['from_'] if self.nick != data['from_'] else data['to_']
            log = "[%s] <%s> %s" %(strftime("%H:%M:%S"), data['from_'], data['msg'])
            self.barnamy_log.set_prv_log(log, with_)

    def lineReceived(self, data):
        self.unpacker.feed(data)
        data = self.unpacker.unpack()
        
        if self.schema.status_schema_f(data): self.app.recv_status_before_login(data)

        if self.schema.status_schema_user_f(data): self.app.barnamy_chat_window_ins.recv_status_user(data)

        if self.schema.login_nok_schema_f(data): self.app.recv_login_nok(data)

        if self.schema.error_schema_f(data): self.app.recv_error_schema(data)

        if self.schema.info_user_schema_user_f(data): self.app.barnamy_chat_window_ins.recv_info_user(data)

        if self.schema.user_join_left_schema_f(data):
            self.app.barnamy_chat_window_ins.recv_user_join_left(data)
            self.app.barnamy_chat_window_ins.barnamy_user_list.recv_user_join_left_prv(data)
            self.barnamy_actions['_notify']("Barnamy", data['user_join_left'])

        if self.schema.access_folder_schema_f(data):
            self.app.barnamy_chat_window_ins.recv_access_folder(data)
            self.barnamy_sound_setting['access_folder_sound']()

        if self.schema.access_folder_valid_schema_f(data):
            self.app.barnamy_chat_window_ins.recv_access_folder_valid(data)

        if self.schema.login_schema_f(data):
            self.token_id = data["token_id"]
            self.nick = data["nick"]
            self.app.recv_login_users(data)
            self.barnamy_sound_setting['login_sound']()

        if self.schema.register_schema_f(data):
            self.app.recv_register(data)

        if self.schema.public_message_f(data):
            self.app.barnamy_chat_window_ins.recv_public_msg(data)
            if self.barnamy_setting_i.get_settings()['log']:
                data['nick'] = data['from_']
                self.barnamy_actions['_log'](data)

        if self.schema.private_message_f(data):
            self.app.barnamy_chat_window_ins.barnamy_user_list.recv_prv_msg(data)
            self.barnamy_sound_setting['received_prv_msg_sound']()
            self.barnamy_actions['_notify']( data['from_'], data['msg'])
            self.barnamy_actions['_prv_log'](data)

        if self.schema.kick_schema_user_f(data):
            print data

    def paste_bin(self, data):
        if data[0] == "fpaste":
            url = BRP.fpaste_scsys(data[1], data[2], data[3])
        elif data[0] == "bpaste":
            url = BRP.bpaste(data[1])
        return url

    def start_web_server(self):
        if os.path.exists(BARNAMY_MINI_WEB_SRV_PID): 
            return True
        else:
            if self.get_settings()['web_tls']:
                self._pid = subprocess.Popen(['twistd', '--pidfile=/tmp/barnamyminisrv.pid', '-n', 'web', 
                '--https=%s'%self.get_settings()['web_tls_port'], 
                '--certificate=%s/barnamy.crt'%self.get_settings()['web_tls_path'], 
                '--privkey=%s/barnamy.key'%self.get_settings()['web_tls_path'],'--resource-script',
                'Base/MiniShareServer/EngineShareServer.rpy', '--port', '%s'%self.get_settings()['wport'] ]) #start
            else :
                self._pid = subprocess.Popen(['twistd', '--pidfile=/tmp/barnamyminisrv.pid', '-n', 'web', 
                                              '--resource-script', 
                'Base/MiniShareServer/EngineShareServer.rpy', '--port', '%s'%self.get_settings()['wport'] ]) #start
            return False

    def stop_web_server(self):
        if self._pid:
            os.kill(self._pid.pid, signal.SIGTERM)
            self._pid = None

    def accept_share(self, nick):
        passwd = None
        if not os.path.exists(BARNAMY_HTTP_PASSWD_FILE):
            passwd_f = open(BARNAMY_HTTP_PASSWD_FILE, 'w+')

        passwd_f = open(BARNAMY_HTTP_PASSWD_FILE, 'r')
        exist = False
        for passwd_l in passwd_f:
            if passwd_l.split(':')[0] == nick:
                exist = True
                passwd = passwd_l.split(':')[1]
                break

        if not exist:
            BARNAMY_HOME_NICK = "%s/%s" %(BARNAMY_HOME, nick)
            if not os.path.exists(BARNAMY_HOME_NICK):
                os.makedirs(BARNAMY_HOME_NICK)
            passwd_f = open(BARNAMY_HTTP_PASSWD_FILE, 'a')
            passwd = ''.join(random.choice(string.ascii_uppercase + string.digits + string.lowercase) for _ in range(11))
            passwd_f.write("%s:%s\n"%(nick, passwd))
            passwd_f.close()

        data = {'type':'access_folder_valid', 'from_':self.nick, 'to_':nick, 'passwd':passwd, 'token_id':self.token_id}
        self.sendLine(self.packer.pack(data))

    def get_info(self, nick):
        data = {'type':'info', 'from_' : self.nick , 'nick' : nick, 'token_id':self.token_id}
        self.sendLine(self.packer.pack(data))

    def ignore_user(self, nick):
        data = {'type':'ignore', 'nick':nick, 'token_id':self.token_id}
        self.sendLine(self.packer.pack(data))

    def unignore_user(self, nick):
        data = {'type':'unignore', 'nick':nick, 'token_id':self.token_id}
        self.sendLine(self.packer.pack(data))

    def call_quote(self):
        quote = None
        if self.get_settings()['tls']:
            response = urllib2.urlopen("https://" + self.get_settings()['ip'] + ":8083")
            quote = json.load(response)
        else:
             response = urllib2.urlopen("http://" + self.get_settings()['ip'] + ":8081")
             quote = json.load(response)
        
        return quote

    def play_false_king_theme(self):
        self.BarnamyPlayer.play_false_king_theme()

    def stop_false_king_theme(self):
        self.BarnamyPlayer._stop_file()

    # it is not implemented yet
    def get_msg_sent_up(self):
        pass

    # it is not implemented yet
    def get_msg_sent_down(self):
        pass

    def set_msg_sent(self, msg):
        self.msg_sent_list.append(msg)
        self.msg_sent_position = len(self.msg_sent_list) - 1

    # It is not resolved
    def kick_user(self, data):
        self.sendLine(self.packer.pack(data))

class BarnamyClientFactory(ReconnectingClientFactory):
    protocol = BarnamyClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed Please verify your settings:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

