# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 21:18:40 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from twisted.internet import reactor
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
from BarnamySettingsGui import BarnamySettingsGui
from BarnamyNewUser import BarnamyNewUser
from BarnamyChatViewer import BarnamyChatViewer
from BarnamyUserList import BarnamyUserList
from BarnamyDialogWarning import BarnamyDialogAbout
from BarnamyPasteBinGui import BarnamyPasteBinGui
import re

class BarnamyChatWindow(Gtk.ApplicationWindow):

    def __init__(self, Base, login_win):
        if Base:
            self.BarnamyBase = Base

        Gtk.Window.__init__(self, title="Barnamy World for the love of community [%s]" %self.BarnamyBase.nick)        
        self.connect("delete-event", Gtk.main_quit)
        self.connect("delete-event", self.barnamy_close)
        self.connect('focus-in-event', self.lost_hint)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Barnamy World - For the love of community [%s]" %self.BarnamyBase.nick
        self.set_titlebar(hb)
        self.set_icon(login_win.barnamy_pixbuf)
        self.bt_nick = Gtk.Button(self.BarnamyBase.nick)
        self.statusbar = Gtk.Statusbar()

        chat_view_scrollbar = Gtk.ScrolledWindow()
        entry_view_scrollbar = Gtk.ScrolledWindow()
        user_list_scrollbar = Gtk.ScrolledWindow()
        chat_view_scrollbar.set_hexpand(True)
        chat_view_scrollbar.set_vexpand(True)
        entry_view_scrollbar.set_hexpand(True)
        entry_view_scrollbar.set_vexpand(True)

        barnamy_login_button_menu = Gtk.MenuButton()
        barnamy_login_button_menu.set_size_request(80, 35)
        hb.pack_start(barnamy_login_button_menu)
        
        menumodel = Gio.Menu()
        menumodel.append("Settings", "win.settings")
        menumodel.append("About", "win.about")
        menumodel.append("Logout", "win.logout")

        self.barnamy_text_chat_view = BarnamyChatViewer()
        chat_view_scrollbar.add(self.barnamy_text_chat_view)
        chat_view_scrollbar.set_shadow_type(Gtk.ShadowType.IN)
        self.banramy_text_chat_enter = Gtk.Entry()
        self.barnamy_user_list = BarnamyUserList(self.BarnamyBase)
        user_list_scrollbar.add(self.barnamy_user_list)
        user_list_scrollbar.set_shadow_type(Gtk.ShadowType.IN)
        self.banramy_text_chat_enter.connect('key-press-event', self.send_msg)
        self.banramy_text_chat_enter.connect('focus-out-event', self.focus_to_entry)

        main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        main_chat_box.set_border_width(7)
        entry_box.set_border_width(5)

        main_paned.set_position(200)
        main_paned.set_wide_handle(True)

        main_paned.add1 (user_list_scrollbar)
        main_paned.add2(main_chat_box)
        main_chat_box.pack_start(chat_view_scrollbar, True, True, 0)        
        main_chat_box.pack_start(entry_box, False, False, 0)
        entry_box.pack_start(self.bt_nick, False, False, 0)
        entry_box.pack_start(self.banramy_text_chat_enter, True, True, 0)

        self.settings_ins = BarnamySettingsGui(self.BarnamyBase)
        self.barnamy_paste_bin_ins = BarnamyPasteBinGui(self.BarnamyBase, self.banramy_text_chat_enter)
        self.barnamy_new_user_ins = BarnamyNewUser(self)

        barnamy_login_button_menu.set_menu_model(menumodel)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("logout", None)
        quit_action.connect("activate", self.barnamy_close)
        self.add_action(quit_action)

        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.barnamy_settings)
        self.add_action(settings_action)

        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        vbox1.pack_start(main_paned, True, True, 0)
        vbox1.set_border_width(7)

        vbox1.pack_end(self.statusbar, False, True, 0)
        self.add(vbox1)
        self.maximize()
        self.login_win = login_win
        self.barnamy_chat_win_state = False

    def focus_to_entry(self, widget, even):
        widget.grab_focus()

    def search_user_to_change_status(self, p_user, status):

        for users in self.barnamy_user_list.user_liststore:
            if users[0] == p_user:
                if status == "Away": users[1] = "Away"
                else: users[1] = "Online"

    def send_status_to_new_user(self, my_nick, nick):
        for users in self.barnamy_user_list.user_liststore:
            if users[0] == my_nick:
                data = {'type':'status', 'nick':my_nick, 'status':users[1], 'token_id':self.BarnamyBase.token_id}
                if users[1] == 'Away':
                    self.BarnamyBase.barnamy_status['away'](data)
                else:
                    self.BarnamyBase.barnamy_status['online'](data)

    def send_msg(self, widget, event):
        #need to be implemented
        if event.keyval == 65362:
            pass

        #need to be implemented
        elif event.keyval == 65364:
            pass

        elif event.keyval == 65293:
            widget.emit_stop_by_name("key-press-event")
            msg = widget.get_text()
            widget.set_text('')
            
            if msg:
                self.BarnamyBase.set_msg_sent(msg)
                if msg.startswith('/'):
                    if msg == '/help':
                        self.barnamy_text_chat_view.put_help_(self.BarnamyBase.barnamy_cmd)
                    elif msg == '/flkg':
                        self.BarnamyBase.barnamy_sound_setting['play_false_king_theme']()
                    elif msg == '/pastebin':
                        self.barnamy_paste_bin_ins.show_all()
                    elif msg == '/stop_flkg':
                        self.BarnamyBase.barnamy_sound_setting['stop_false_king_theme']()
                    elif msg == '/run_srv':
                        self.BarnamyBase.barnamy_actions['start_web_server']()
                    elif msg == '/stop_srv':
                        self.BarnamyBase.barnamy_actions['stop_web_server']()
                    elif msg == '/away':
                        self.search_user_to_change_status(self.BarnamyBase.nick, "Away")
                        data = {'type':'status', 'nick':self.BarnamyBase.nick, 'status':'Away', 
                                'token_id':self.BarnamyBase.token_id}
                        self.BarnamyBase.barnamy_status['away'](data)
                    elif msg == '/online':
                        self.search_user_to_change_status(self.BarnamyBase.nick, "Online")
                        data = {'type':'status', 'nick':self.BarnamyBase.nick, 'status':'Online', 
                                'token_id':self.BarnamyBase.token_id}
                        self.BarnamyBase.barnamy_status['away'](data)
                    elif msg == '/quote':
                        self.barnamy_text_chat_view.put_barnamy_quote(self.BarnamyBase.barnamy_actions['call_quote']())
                    elif msg.startswith('/ignore') and len(msg.split(' ')[1:]) == 1:
                        self.BarnamyBase.barnamy_actions['ignore_user'](msg.split(' ')[1])
                    elif msg.startswith('/unignore') and len(msg.split(' ')[1:]) == 1:
                        self.BarnamyBase.barnamy_actions['unignore_user'](msg.split(' ')[1])
                    elif msg.startswith('/allow') and len(msg.split(' ')[1:]) == 1:
                        self.BarnamyBase.barnamy_actions['accept_share'](msg.split(' ')[1])
                    elif msg.startswith('/admin') and len(msg.split(' ')[1:]) >= 1:
                        data = {"type":"admin", "nick":self.BarnamyBase.nick, 
                                "token_id":self.BarnamyBase.token_id, 
                                "msg":msg.split(' ')[1]}
                        self.BarnamyBase.barnamy_actions['send_pub_msg'](data)
                    elif msg.startswith('/info') and len(msg.split(' ')[1:]) == 1:
                        self.BarnamyBase.barnamy_actions['get_info'](msg.split(' ')[1])
                    elif msg.startswith('/kick') and len(msg.split(' ')[1:]) == 1:
                        data = {'type':'kick', 'from_' : self.BarnamyBase.nick, 'nick' : msg.split(' ')[1],
                                'token_id':self.BarnamyBase.token_id}
                        self.BarnamyBase.barnamy_actions['kick_user'](data)

                    #prvmsg command needs a rewrite
                    elif msg.startswith('/prvmsg'):
                        delay = msg.split(' ', 2)[1]
                        users_msgs = msg.split(' ', 2)[2]

                        if users_msgs:
                            for user_msg in users_msgs.split(','):
                                nick = user_msg.split(':')[0]
                                prv_msg = user_msg.split(':')[1]
                                if nick in self.barnamy_user_list.user_liststore[0]:
                                    data = {'type' : 'private', 'to_' : nick , 'from_' : self.BarnamyBase.nick,
                                        'token_id' : self.BarnamyBase.token_id, 'msg' : prv_msg.strip()}
                                    self.BarnamyBase.barnamy_actions['prv_msg_cmd'](delay, data)

                    else:
                        self.barnamy_text_chat_view.put_help_(self.BarnamyBase.barnamy_cmd)
                    return

                self.barnamy_text_chat_view.put_msg_(self.BarnamyBase.nick, msg)
                data = {'type' : 'public', 'nick' : self.BarnamyBase.nick, 
                        'token_id' : self.BarnamyBase.token_id, 'msg' : msg}
                self.BarnamyBase.barnamy_actions['send_pub_msg'](data)
                return

    def recv_user_join_left(self, data):
        self.barnamy_user_list.update_users_list(data['user'])
        if data['user'] in data['user_list']:
            self.send_status_to_new_user(self.BarnamyBase.nick, data['user'])

            if not data['user'] in self.barnamy_text_chat_view.users_tag:
                self.barnamy_text_chat_view.users_tag[data['user']] = self.barnamy_text_chat_view.radom_color(data['user'])

        self.barnamy_text_chat_view.recv_left_joing(data['user_join_left'])

    def recv_public_msg(self, data):
        user_in_msg = re.match("\w*\s*(%s)\w*\s*"%self.BarnamyBase.nick, data['msg'])
        if user_in_msg:
            self.set_urgency_hint(True)
            self.barnamy_text_chat_view.rcev_msg_highlight(data['from_'], data['msg'])
            return
        self.barnamy_text_chat_view.rcev_msg(data['from_'], data['msg'])

    def recv_access_folder(self, data):
        self.barnamy_text_chat_view.put_folder_access(data['from_'])

    def recv_access_folder_valid(self, data):
        self.barnamy_text_chat_view.put_folder_access_valid(data['from_'], data['passwd'])

    def recv_status_user(self, data):
        self.search_user_to_change_status(data['nick'], data['status'])

    def recv_info_user(self, data):
        self.barnamy_text_chat_view.put_user_info(data['nick'], data['info'])

    def lost_hint(self, widget, event):
        self.set_urgency_hint(False)

    def about_callback(self, action, parameter):
        BarnamyDialogAbout(self).run()

    def barnamy_close(self, widget, event):
        data = {'type' : 'logout', 'nick' : self.BarnamyBase.nick, 'token_id' : self.BarnamyBase.token_id}
        self.BarnamyBase.barnamy_actions['do_logout'](data)
        self.barnamy_text_chat_view.chat_buffer.set_text('')
        self.banramy_text_chat_enter.set_text('')
        self.hide()
        self.login_win.show_all()
        self.barnamy_chat_win_state = False
        self.BarnamyBase.barnamy_actions['stop_web_server']()
        barnamy_tag_table = self.barnamy_text_chat_view.chat_buffer.get_tag_table()
        for user in self.barnamy_text_chat_view.users_tag:
            tag = barnamy_tag_table.lookup(user)
            if tag:
                barnamy_tag_table.remove(tag)

    def RunBarnamyChatWindow(self):
        self.barnamy_chat_win_state = True    
        self.show_all()
        context_id = self.statusbar.get_context_id("barnamy")
        message_id = self.statusbar.push(context_id, 'connected to barnamy as %s'%self.BarnamyBase.nick)
        self.banramy_text_chat_enter.grab_focus()
        self.barnamy_text_chat_view.barnamy_welcome()
        self.barnamy_text_chat_view.users_tag[self.BarnamyBase.nick] = self.barnamy_text_chat_view.chat_buffer.create_tag("user_color", foreground="#0000FF")

    def barnamy_settings(self, action, parameter):
        self.settings_ins.barnamy_settings_open()

