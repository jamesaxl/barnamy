# -*- coding: utf-8 -*-
from twisted.internet import gtk3reactor
gtk3reactor.install()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Pango, Gdk
from twisted.internet import reactor
from time import gmtime, strftime
import sys
import os
import random
import re
import cairo
import webbrowser

class BarnamyClientGui(object):
    
    def __init__(self, Base = 0):
        if Base:
            self.BarnamyBase = Base

        self.hovering_over_link = False
        self.chat_buffer = None
        self.color_dic = {}
        self.hint_prv = False
        self.hint_public = False
        self.pastebin_msg = False
        self.nick = None
        self.token_id = None
        self.selected_user = None
        self.selected_prv_chat = None
        self.position = 0
        self.current_user = None
        self._builder = Gtk.Builder()
        self._builder.add_from_file("Theme/GuiGtk/barnamy_ui.glade")
        self._winchat_state = False
        self.access_folder_state = False
        self.barnamy_widget = {}
        self.barnamy_widget_prv_chat = {}
        self.users_access = []
        self.pre_login = {}
        self.post_login = {}

        self.barnamy_widget["barnamy_login"] = self._builder.get_object("barnamyWindowLogin")
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Barnamy Login"
        self.barnamy_widget["barnamy_login"].set_titlebar(hb)
        self.barnamy_widget["barnamy_pastebin"] = self._builder.get_object("barnamy_pastebin")
        self.barnamy_widget["cb_pastebin"] = self._builder.get_object("cb_pastebin")
        self.barnamy_widget["send_pastebin"] = self._builder.get_object("send_pastebin")
        self.barnamy_widget["pastebin_close"] = self._builder.get_object("pastebin_close")
        self.barnamy_widget["barnamy_status_icon"] = self._builder.get_object("barnamy_status_icon")
        self.barnamy_widget['aboutdialog_buttons'] = self._builder.get_object("aboutdialog_buttons")
        self.barnamy_widget["status_menu"] = self._builder.get_object("status_menu")
        self.barnamy_widget["status_disconnect"] = self._builder.get_object("status_disconnect")
        self.barnamy_widget["online_item"] = self._builder.get_object("online_item")
        self.barnamy_widget["away_status"] = self._builder.get_object("away_status")
        self.barnamy_widget["close_status"] = self._builder.get_object("close_status")
        self.barnamy_widget["item_preferences"] = self._builder.get_object("item_preferences")
        self.barnamy_widget["item_preferences_chat"] = self._builder.get_object("item_preferences_chat")
        self.barnamy_widget["switch_notify"] = self._builder.get_object("switch_notify")
        self.barnamy_widget["switch_log"] = self._builder.get_object("switch_log")
        self.barnamy_widget["switch_tls"] = self._builder.get_object("switch_tls")
        self.barnamy_widget["status_disconnect"] = self._builder.get_object("status_disconnect")
        self.barnamy_widget["barnamy_nick_enter"] = self._builder.get_object("e_nick")
        self.barnamy_widget["barnamy_passwd_enter"] = self._builder.get_object("e_passwd")
        self.barnamy_widget["barnamy_bt_login"] = self._builder.get_object("bt_login")
        self.barnamy_widget["barnamy_login_status"] = self._builder.get_object("status_bar_login")
        self.barnamy_widget["aboutBarnamy"] = self._builder.get_object("aboutBarnamy")
        self.barnamy_widget["item_quit"] = self._builder.get_object("item_quit")
        self.barnamy_widget["item_about"] = self._builder.get_object("item_about")
        self.barnamy_widget["item_register"] = self._builder.get_object("item_register")
        self.barnamy_widget["singleChat"] = self._builder.get_object("singleChat")
        self.barnamy_widget["item_about_chat"] = self._builder.get_object("item_about_chat")
        self.barnamy_widget["barnamy_chat_window"] = self._builder.get_object("barnamyChatWindow")
        self.barnamy_widget["barnamy_text_enter"] = self._builder.get_object("text_enter")
        self.barnamy_widget["barnamy_text_chat"] = self._builder.get_object("text_chat")
        self.barnamy_widget["barnamy_text_enter"].grab_focus()
        self.barnamy_widget["barnamy_user_list"] = self._builder.get_object("user_tree_view")
        self.barnamy_widget["item_disconnect"] = self._builder.get_object("item_disconnect")
        self.barnamy_widget["group_users"] = self._builder.get_object("group_users")
        self.barnamy_widget["user_menu"] = self._builder.get_object("user_menu")
        self.barnamy_widget["prv_msg"] = self._builder.get_object("prv_msg")
        self.barnamy_widget["folder_share_access"] = self._builder.get_object("folder_share_access")
        self.barnamy_widget["access_order"] = self._builder.get_object("access_order")
        self.barnamy_widget["l_count"] = self._builder.get_object("l_count")
        self.barnamy_widget["user_nick"] = self._builder.get_object("user_nick")
        self.barnamy_widget["bt_back"] = self._builder.get_object("bt_back")
        self.barnamy_widget["bt_forward"] = self._builder.get_object("bt_forward")
        self.barnamy_widget["bt_close_access"] = self._builder.get_object("bt_close_access")
        self.barnamy_widget["bt_cancel_access"] = self._builder.get_object("bt_cancel_access")
        self.barnamy_widget["bt_access_ok"] = self._builder.get_object("bt_access_ok")
        self.barnamy_widget["register_window"] = self._builder.get_object("register_window")
        self.barnamy_widget["barnamy_register_status"] = self._builder.get_object("barnamy_register_status")
        self.barnamy_widget["entry_nick"] = self._builder.get_object("entry_nick")
        self.barnamy_widget["entry_passwd"] = self._builder.get_object("entry_passwd")
        self.barnamy_widget["entry_cf_passwd"] = self._builder.get_object("entry_cf_passwd")
        self.barnamy_widget["entry_email"] = self._builder.get_object("entry_email")
        self.barnamy_widget["bt_register"] = self._builder.get_object("bt_register")
        self.barnamy_widget["baramy_settings"] = self._builder.get_object("baramy_settings")
        self.barnamy_widget["bt_save_settings"] = self._builder.get_object("bt_save_settings")
        self.barnamy_widget["bt_close_setting"] = self._builder.get_object("bt_close_setting")
        self.barnamy_widget["entry_ip"] = self._builder.get_object("entry_ip")
        self.barnamy_widget["entry_port"] = self._builder.get_object("entry_port")
        self.barnamy_widget["entry_wport"] = self._builder.get_object("entry_wport")
        self.barnamy_widget["switch_sound"] = self._builder.get_object("switch_sound")
        self.barnamy_widget["bt_barnamy_web_server"] = self._builder.get_object("bt_barnamy_web_server")
                
        self.textbuffer = self.barnamy_widget["barnamy_text_chat"].get_buffer()
        self.user_tag = self.textbuffer.create_tag("user_color", foreground="#0000FF")
        self.highlight = self.textbuffer.create_tag("highlight", foreground="#BB0000")
        self.join_left_cmd_tag = self.textbuffer.create_tag("join_left", foreground="#999999")
        self.bold = self.textbuffer.create_tag( "bold", weight=Pango.Weight.BOLD)
        self.user_liststore = Gtk.ListStore(str, str)
        users_rend = Gtk.CellRendererText()
        status_rend = Gtk.CellRendererText()
        users_col = Gtk.TreeViewColumn("Users", users_rend, text=0)
        status_col = Gtk.TreeViewColumn("Status", status_rend, text=1)

        self.barnamy_widget["barnamy_nick_enter"].connect('key-press-event', self.do_login_enter_press)
        self.barnamy_widget["barnamy_passwd_enter"].connect('key-press-event', self.do_login_enter_press)
        self.barnamy_widget["singleChat"].connect('focus-in-event', self.focus_in_private_chat)
        self.barnamy_widget["barnamy_chat_window"].connect('focus-in-event', self.focus_in_public_chat)
        self.barnamy_widget["singleChat"].connect('focus-out-event', self.focus_out_private_chat)
        self.barnamy_widget["barnamy_chat_window"].connect('focus-out-event', self.focus_out_public_chat)
        self.barnamy_widget["barnamy_text_chat"].connect('motion-notify-event', self.motion_notify_event)
        self.barnamy_widget["barnamy_status_icon"].connect('button-press-event', self.status_press_button)
        self.barnamy_widget["item_register"].connect('activate', self.RegisterWindow)
        self.barnamy_widget["item_quit"].connect('activate', self.stop)
        self.barnamy_widget["item_preferences_chat"].connect('activate', self.barnamy_settings_open)
        self.barnamy_widget["item_preferences"].connect('activate', self.barnamy_settings_open)
        self.barnamy_widget["item_about"].connect('activate', self.about_barnamy)
        self.barnamy_widget["barnamy_login"].connect('delete-event', self.close_to_status)
        
        self.barnamy_widget["singleChat"].connect('delete-event', self.hide_private_chat)
        self.barnamy_widget["item_about_chat"].connect('activate', self.about_barnamy)
        self.barnamy_widget["barnamy_chat_window"].connect('delete-event', self.close_to_status)
        self.barnamy_widget["access_order"].connect('delete-event', self.HideAccessOrder)
        self.barnamy_widget["bt_close_access"].connect("clicked", self.HideAccessOrder)
        self.barnamy_widget["register_window"].connect('delete-event', self.hide_register_win)
        self.barnamy_widget["aboutBarnamy"].connect('delete-event', self.hide_about_barnamy)
        self.barnamy_widget["barnamy_user_list"].append_column(users_col)
        self.barnamy_widget["barnamy_user_list"].append_column(status_col)
        self.barnamy_widget["barnamy_user_list"].set_model(self.user_liststore)
        self.barnamy_widget["barnamy_text_enter"].connect('key-press-event', self.send_public_msg)
        self.barnamy_widget["barnamy_bt_login"].connect("clicked", self.do_login)
        self.barnamy_widget["item_disconnect"].connect("activate", self.do_logout)
        self.barnamy_widget["prv_msg"].connect('activate', self.RunBarnamySingleChat)
        self.barnamy_widget["folder_share_access"].connect('activate', self.ask_to_access_forlder)
        self.barnamy_widget["bt_back"].connect("clicked", self.back)
        self.barnamy_widget["bt_forward"].connect("clicked", self.forward)
        self.barnamy_widget["bt_access_ok"].connect("clicked", self.accept)
        self.barnamy_widget["bt_cancel_access"].connect("clicked", self.cancel)
        self.barnamy_widget["barnamy_user_list"].connect('button_press_event', self.on_user_list_button_press_event)
        self.barnamy_widget["barnamy_user_list"].connect('button_press_event', self.on_user_list_double_click)
        self.barnamy_widget["barnamy_user_list"].get_selection().connect("changed", self.on_selected_user_change)
        self.barnamy_widget["group_users"].connect('switch-page', self.get_user_win_prv_title)
        self.barnamy_widget["online_item"].set_active(True)
        self.barnamy_widget["bt_register"].connect("clicked", self.regiser_new_user)
        self.barnamy_widget["online_item"].connect("toggled", self.status_online)
        self.barnamy_widget["away_status"].connect("toggled", self.status_away)
        self.barnamy_widget["status_disconnect"].connect("activate", self.do_logout)
        self.barnamy_widget["close_status"].connect("activate", self.stop)
        self.barnamy_widget["bt_close_setting"].connect("clicked", self.barnamy_settings_close)
        self.barnamy_widget["baramy_settings"].connect("delete-event", self.barnamy_settings_close)
        self.barnamy_widget["bt_save_settings"].connect("clicked", self.barnamy_save_setting)
        self.barnamy_widget["send_pastebin"].connect("clicked", self.pastebin_request)
        self.barnamy_widget["barnamy_pastebin"].connect("delete-event", self.pastebin_hide)
        self.barnamy_widget["pastebin_close"].connect("clicked", self.pastebin_hide)
        self.barnamy_widget["bt_barnamy_web_server"].connect("clicked", self.start_web_server)
        
        for button in self.barnamy_widget['aboutdialog_buttons']:
            self.barnamy_widget['aboutdialog_buttons'] = button
        self.barnamy_widget['aboutdialog_buttons'].connect("clicked", self.hide_about_barnamy)

    def start_web_server(self, widget = 0):
        if self.barnamy_widget["bt_barnamy_web_server"].get_label() == 'Run':
            self.BarnamyBase.barnamy_actions['start_web_server']()
            self.barnamy_widget["bt_barnamy_web_server"].set_label('Stop')
        elif self.barnamy_widget["bt_barnamy_web_server"].get_label() == 'Stop':
            self.stop_web_server()

    def stop_web_server(self):
        self.BarnamyBase.barnamy_actions['stop_web_server']()
        self.barnamy_widget["bt_barnamy_web_server"].set_label('Run')

    def radom_color(self, user):
        colors = ['#FF0000', '#FF0088', '#FF00FF', '#8400FF', '#0000FF', 
        '#0084FF', '#00FF84', '#00FF00', '#FF8000', '#008800']
        return self.textbuffer.create_tag(user, foreground=random.choice(colors))

    def status_press_button(self, widget = 0, event = 0):
        if event.button == 1:
            self.close_to_status()
        elif event.button == 3:
            self.barnamy_widget["status_menu"].popup(None, None, None, None, event.button, event.time)

    def close_to_status(self, widget = 0, event = 0):
        if self.pre_login['win'] and self.pre_login['state']:
            self.HideBarnamyLogin()
            self.pre_login['state'] = False
        elif self.pre_login['win'] and self.pre_login['state'] == False:
            self.RunBarnamyLogin()

        if self.post_login['win'] and self.post_login['state']:
            self.HideBarnamyChat()
            self.post_login['state'] = False
        elif self.post_login['win'] and self.post_login['state'] == False:
            self.RunBarnamyChat()
        return True

    def RunBarnamyLogin(self):
        self.barnamy_widget["barnamy_login"].show_all()
        self.pre_login['win'] = True
        self.pre_login['state'] = True
        self.post_login['win'] = False
        self.post_login['state'] = False
        
    def RunBarnamyChat(self):
        self.barnamy_widget["barnamy_chat_window"].show_all()
        self.post_login['win'] = True
        self.post_login['state'] = True
        self.pre_login['win'] = False
        self.pre_login['state'] = False

    def HideBarnamyLogin(self):
        self.barnamy_widget["barnamy_login"].hide()

    def HideBarnamyChat(self):
        text_buffer = self.barnamy_widget["barnamy_text_enter"].get_buffer()
        text_buffer.set_text("")
        text_buffer = self.barnamy_widget["barnamy_text_chat"].get_buffer()
        if not self.post_login['state']:
            text_buffer.set_text("")
        self.barnamy_widget["barnamy_chat_window"].hide()

    def build_single_chat(self):
        return self._winchat_state
    
    def about_barnamy(self, widget):
        result = self.barnamy_widget["aboutBarnamy"].run()

    def pastebin_barnamy(self, msg, text_buffer):
        self.chat_buffer = text_buffer
        self.pastebin_msg = msg
        self.barnamy_widget["barnamy_pastebin"].show_all()

    def pastebin_request(self, widget):
        text_buffer = self.chat_buffer.get_buffer()
        if self.barnamy_widget["cb_pastebin"].get_active_text() == "paste.scsys":
            url = self.BarnamyBase.pastebin(("paste.scsys", self.nick, "barnamy pastebin", self.pastebin_msg))
        elif self.barnamy_widget["cb_pastebin"].get_active_text() == "bpaste":
            url = self.BarnamyBase.pastebin(("bpaste", self.pastebin_msg))

        text_buffer.set_text(url)
        self.pastebin_hide()
        return True

    def pastebin_hide(self, widget=0, event=0):
        self.barnamy_widget["barnamy_pastebin"].hide()
        return True

    def hide_private_chat(self, widget = 0, event = 0):
        for page in range(0, self.barnamy_widget["group_users"].get_n_pages()):
            self.barnamy_widget["group_users"].remove_page(0)

	self.barnamy_widget_prv_chat.clear()
        self.barnamy_widget["singleChat"].hide()
        return True

    def hide_register_win(self, widget, event):
        self.barnamy_widget["register_window"].hide()
        self.barnamy_widget["entry_nick"].set_text("")
        self.barnamy_widget["entry_passwd"].set_text("")
        self.barnamy_widget["entry_cf_passwd"].set_text("")
        self.barnamy_widget["entry_email"].set_text("")
        return True

    def ObjectGui(self, widget, text = None):
	if widget == "TextView":
	    return Gtk.TextView()
	if widget == "Label":
	    hbox = Gtk.Box(spacing=6)
	    label = Gtk.Label(label="%s" %str(text))
	    button = Gtk.Button("X")
	    button.connect('clicked', self.on_closetab_button_clicked, hbox)
	    hbox.pack_start(label, True, True, 0)
	    hbox.pack_start(button, False, False, 0)
	    hbox.show_all()
	    return hbox
	if widget == "double_click":
	    return Gdk.EventType.DOUBLE_BUTTON_PRESS
        if widget == "Paned" and text == "vertical":
            return Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        if widget == "ScrolledWindow":
            return Gtk.ScrolledWindow()

    def on_closetab_button_clicked(self, sender, widget):
        nick = widget.get_children()[0].get_text()
        del self.barnamy_widget_prv_chat[nick]
        pagenum = self.barnamy_widget["group_users"].page_num(widget)
        if self.barnamy_widget["group_users"].get_n_pages() == 1:
            self.barnamy_widget["singleChat"].hide()
        self.barnamy_widget["group_users"].remove_page(pagenum)

    def RegisterWindow(self, widget):
        self.barnamy_widget["register_window"].show_all()

    def RunAccessOrder(self):
        if self.access_folder_state == False:
            self.barnamy_widget["access_order"].show_all()
            self.access_folder_state = True

    def HideAccessOrder(self, widget = 0, event = 0):
        self.barnamy_widget["access_order"].hide()
        self.access_folder_state = False
        del self.users_access[:]
        return True

    def UnicodeEmoticonsList(self, emoticon):
        if emoticon == ":-)":
            return u"\U0001F60A"
        elif emoticon == ":D":
            return u"\U0001f600"
        elif emoticon == ":(":
            return u"\U0001F61E"
        elif emoticon == ":p":
            return u"\U0001F61B"
        elif emoticon =="o:)":
            return u"\U0001f607"
        elif emoticon =="3:)":
            return u"\U0001f608"

    def EmoticonsFilter(self, msg):
        filter = re.findall(":-\)|:D|3:\)|o:\)|:\(|:p", msg)
        if filter:
            for i in filter:
                msg = msg.replace(i, self.UnicodeEmoticonsList(i))
            return msg
        return False

    def stop(self, widget = 0):
        reactor.stop()

    def recv_status_before_connexion(self, data):
        context_id = self.barnamy_widget["barnamy_login_status"].get_context_id("Barnamy")
        message_id = self.barnamy_widget["barnamy_login_status"].push(context_id, data["status"])

    def recv_status_user(self, data):
        self.search_user_to_change_status(data['nick'], data['status'])

    def recv_login_nok(self, data):
        dialog = Gtk.MessageDialog(self.barnamy_widget['barnamy_login'], 0, Gtk.MessageType.WARNING,
        Gtk.ButtonsType.OK, "Barnamy Warning")
        dialog.format_secondary_text(data['msg'])
        dialog.run()
        dialog.destroy()

    def recv_error_schema(self, data):
        dialog = Gtk.MessageDialog(self.barnamy_widget['register_window'], 0, Gtk.MessageType.WARNING,
        Gtk.ButtonsType.OK, "Barnamy Warning")
        dialog.format_secondary_text("nick should 4 chars to 10 chars\nemail should be valid\npassword should be min 6 chars")
        dialog.run()
        dialog.destroy()

    def recv_user_join_left(self, data):
        self.user_liststore.clear()
        data['user_list'].sort()
        for user in data['user_list']:
            self.user_liststore.append([user, "Online"])
            if not user in self.color_dic and user!= self.nick:
                self.color_dic[user] =  self.radom_color(user)

        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert_with_tags(end_iter, "[%s] --- %s ---\n"%(strftime("%H:%M:%S", gmtime()), data["user_join_left"]), 
                                         self.join_left_cmd_tag)
        if not data['user'] in data['user_list'] and data['user'] in self.barnamy_widget_prv_chat.keys():
            self.barnamy_widget_prv_chat[data['user']]["enter_view"].set_sensitive(False)
            chat_buffer = self.barnamy_widget_prv_chat[data['user']]["chat_view"].get_buffer()
            end_iter = chat_buffer.get_end_iter()
            join_left_tag_prv = chat_buffer.create_tag(None, foreground="#999999")
            chat_buffer.insert_with_tags(end_iter, "[%s] --- %s ---\n"%(strftime("%H:%M:%S", gmtime()), data["user_join_left"]), 
                                         join_left_tag_prv)

        if data['user'] in data['user_list'] and data['user'] in self.barnamy_widget_prv_chat.keys():
            self.barnamy_widget_prv_chat[data['user']]["enter_view"].set_sensitive(True)
            chat_buffer = self.barnamy_widget_prv_chat[data['user']]["chat_view"].get_buffer()
            end_iter = chat_buffer.get_end_iter()
            join_left_tag_prv = chat_buffer.create_tag(None, foreground="#999999")
            chat_buffer.insert_with_tags(end_iter, "[%s] --- %s ---\n"%(strftime("%H:%M:%S", gmtime()), data["user_join_left"]), 
                                         join_left_tag_prv)

    def recv_access_folder(self, data):
        if not data['from_'] in self.users_access:
            self.users_access.append(data['from_'])
            self.barnamy_widget["l_count"].set_text("%d/%d"%(self.position + 1, len(self.users_access)))
            self.barnamy_widget["user_nick"].set_markup("<b>%s</b> sends a request private folder access" %self.users_access[self.position])
            self.RunAccessOrder()

            self.BarnamyBase.barnamy_sound_setting['access_folder_sound']()

    def recv_access_folder_valid(self, data):
        text_buffer = self.barnamy_widget["barnamy_text_chat"].get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags(end_iter, "---%s accepted you, the Password is %s and you should not lose it---\n"%(data['from_'], data['passwd']), 
            self.join_left_cmd_tag)

    def recv_login_users(self, data):
        self.HideBarnamyLogin()
        self.RunBarnamyChat()
        self.token_id = data["token_id"]
        self.nick = data["nick"]
        self.user_liststore.clear()
        data['user_list'].sort()
        for user in data['user_list']:
            self.user_liststore.append([user, "Online"])
            #if not user in self.color_dic and user!= self.nick:
            if user!= self.nick:
                self.color_dic[user] =  self.radom_color(user)
        self.barnamy_widget["barnamy_chat_window"].set_title("%s connected on Barnamy" %self.nick)

        self.BarnamyBase.barnamy_sound_setting['login_sound']()

    def recv_register(self, data):
        context_id = self.barnamy_widget["barnamy_register_status"].get_context_id("Barnamy")
        message_id = self.barnamy_widget["barnamy_register_status"].push(context_id, data["succ"])
        self.barnamy_widget["entry_nick"].set_text("")
        self.barnamy_widget["entry_passwd"].set_text("")
        self.barnamy_widget["entry_cf_passwd"].set_text("")
        self.barnamy_widget["entry_email"].set_text("")

    def recv_public_msg(self, data):
        text_buffer = self.barnamy_widget["barnamy_text_chat"].get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert(end_iter, "[%s] "%strftime("%H:%M:%S", gmtime()))
        
        _log = "barnamy_public_%s"%self.nick, "[%s]<%s>%s\n" %(strftime("%H:%M:%S", gmtime()), data['from_'], data['msg'])
        self.BarnamyBase.barnamy_actions['_log'](_log)
        
        if self.EmoticonsFilter(data["msg"]):
            data['msg'] = self.EmoticonsFilter(data["msg"])
        pattern = "^\w*\s*%s\w*\s*"%self.nick
        p = re.compile(pattern)
        if p.match(data["msg"]):
            end_iter = text_buffer.get_end_iter()
            text_buffer.insert_with_tags(end_iter, "<%s> "%data["from_"], self.highlight)

            for word in data["msg"].split(" "):
                p = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
                end_iter = text_buffer.get_end_iter()
                if p.match(word):
                    if word == data["msg"].split(" ")[-1]:self.insert_link(text_buffer, end_iter, "%s" %word)
                    else:
                        self.insert_link(text_buffer, end_iter, "%s" %word)
                        end_iter = text_buffer.get_end_iter()
                        text_buffer.insert(end_iter, " ")
                else:
                    if word == data["msg"].split(" ")[-1]:text_buffer.insert_with_tags(end_iter, "%s" %word, self.bold)
                    else: text_buffer.insert_with_tags(end_iter, "%s " %word, self.bold)
            text_buffer.insert(end_iter, "\n")

            self.barnamy_widget['barnamy_chat_window'].set_urgency_hint(self.hint_public)
        else:
            end_iter = text_buffer.get_end_iter()
            text_buffer.insert_with_tags(end_iter, "<%s> "%data["from_"], self.color_dic[data["from_"]])

            for word in data["msg"].split(" "):
                p = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
                end_iter = text_buffer.get_end_iter()
                if p.match(word):
                    if word == data["msg"].split(" ")[-1]:self.insert_link(text_buffer, end_iter, "%s" %word)
                    else:
                        self.insert_link(text_buffer, end_iter, "%s" %word)
                        end_iter = text_buffer.get_end_iter()
                        text_buffer.insert(end_iter, " ")
                else:
                    if word == data["msg"].split(" ")[-1]:text_buffer.insert_with_tags(end_iter, "%s" %word, self.bold)
                    else: text_buffer.insert_with_tags(end_iter, "%s " %word, self.bold)
            text_buffer.insert(end_iter, "\n")

    def recv_prv_msg(self, data):
        if not self.build_single_chat():
            self.barnamy_widget["singleChat"].show_all()

        if not data['from_'] in self.barnamy_widget_prv_chat:
            paned = self.ObjectGui("Paned", "vertical")
            paned.set_position(500)
            scrolledwindow_top = self.ObjectGui("ScrolledWindow")
            scrolledwindow_top.set_hexpand(True)
            scrolledwindow_top.set_vexpand(True)
            
            scrolledwindow_bottom = self.ObjectGui("ScrolledWindow")
            scrolledwindow_bottom.set_hexpand(True)
            scrolledwindow_bottom.set_vexpand(True)
            self.barnamy_widget_prv_chat[data['from_']] = {}

            self.barnamy_widget_prv_chat[data['from_']]["chat_view"] = self.ObjectGui("TextView")
            self.barnamy_widget_prv_chat[data['from_']]["chat_view"].set_editable(False)
            self.barnamy_widget_prv_chat[data['from_']]["chat_view"].set_cursor_visible(False)
            self.barnamy_widget_prv_chat[data['from_']]["chat_view"].set_wrap_mode(Gtk.WrapMode.WORD)
            fontdesc = Pango.FontDescription("monospace 10.5")
            self.barnamy_widget_prv_chat[data['from_']]["chat_view"].modify_font(fontdesc)
            
            self.barnamy_widget_prv_chat[data['from_']]["enter_view"] = self.ObjectGui("TextView")
            self.barnamy_widget_prv_chat[data['from_']]["enter_view"].grab_focus()
            self.barnamy_widget_prv_chat[data['from_']]["enter_view"].set_wrap_mode(Gtk.WrapMode.WORD)
            self.barnamy_widget_prv_chat[data['from_']]["enter_view"].connect('key-press-event', self.send_prv_msg)
            scrolledwindow_top.add(self.barnamy_widget_prv_chat[data['from_']]["chat_view"])
            scrolledwindow_bottom.add(self.barnamy_widget_prv_chat[data['from_']]["enter_view"])

            paned.pack1(scrolledwindow_top, True, False)

            paned.pack2(scrolledwindow_bottom, True, False)
            tab = self.ObjectGui("Label", data['from_'])
            self.barnamy_widget["group_users"].append_page(paned, tab)
            self.barnamy_widget["group_users"].set_scrollable(True)
            self.barnamy_widget["group_users"].show_all()

        chat_buffer = self.barnamy_widget_prv_chat[data['from_']]["chat_view"].get_buffer()
        end_iter = chat_buffer.get_end_iter()
        chat_buffer.insert(end_iter, "[%s] "%(strftime("%H:%M:%S", gmtime())))
        end_iter = chat_buffer.get_end_iter()
        from_user = chat_buffer.create_tag(None, foreground='red')
        chat_buffer.insert_with_tags(end_iter, "<%s> "%data['from_'], from_user)

        _log = "barnamy_prv_%s_%s"%(self.nick, data['from_']), "[%s]<%s>%s\n" %(strftime("%H:%M:%S", gmtime()), data['from_'], data['msg'])
        self.BarnamyBase.barnamy_actions['_log'](_log)

        if self.EmoticonsFilter(data["msg"]):
            data['msg'] = self.EmoticonsFilter(data["msg"])

        for word in data["msg"].split(" "):
            p = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            end_iter = chat_buffer.get_end_iter()
            if p.match(word):
                if word == data["msg"].split(" ")[-1]:self.insert_link(chat_buffer, end_iter, "%s" %word)
                else:
                    self.insert_link(chat_buffer, end_iter, "%s" %word)
                    end_iter = chat_buffer.get_end_iter()
                    chat_buffer.insert(end_iter, " ")
            else:
                if word == data["msg"].split(" ")[-1]:chat_buffer.insert(end_iter, "%s" %word)
                else: chat_buffer.insert(end_iter, "%s " %word)
        chat_buffer.insert(end_iter, "\n")

        self.barnamy_widget['singleChat'].set_urgency_hint(self.hint_prv)

        self.BarnamyBase.barnamy_sound_setting['received_prv_msg_sound']()

        self.BarnamyBase.barnamy_actions['_notify']( data['from_'], data['msg'])

    def barnamy_dialog_warning(self, msg):
        dialog = Gtk.MessageDialog(self.barnamy_widget['register_window'], 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Barnamy Warning")
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()
        return

    def regiser_new_user(self, widget):
        if not self.barnamy_widget["entry_nick"].get_text():
            self.barnamy_dialog_warning("Nick required")

        if not self.barnamy_widget["entry_email"].get_text():
            self.barnamy_dialog_warning("Email required")


        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.barnamy_widget["entry_email"].get_text()) == None:
            self.barnamy_dialog_warning("Email not valid")

        if not self.barnamy_widget["entry_passwd"].get_text():
            self.barnamy_dialog_warning("Password required")

        if not self.barnamy_widget["entry_cf_passwd"].get_text():
            self.barnamy_dialog_warning("Password comfirmation required")

        if self.barnamy_widget["entry_passwd"].get_text() != self.barnamy_widget["entry_cf_passwd"].get_text():
            self.barnamy_dialog_warning("Password and Re-password should be the same")

        data = {"type":"register", "nick":self.barnamy_widget["entry_nick"].get_text(), "email":self.barnamy_widget["entry_email"].get_text(), 
                "passwd":self.barnamy_widget["entry_passwd"].get_text()}

        self.BarnamyBase.barnamy_actions['regiser_new_user'](data)

    def send_public_msg(self, widget, event):

        keyval = event.keyval
        name = Gdk.keyval_name(keyval)
        mod = Gtk.accelerator_get_label(keyval, event.state)
        if mod == "Ctrl+Mod2+Return":
            pass
        elif event.keyval == 65293:
            chat_buffer = self.barnamy_widget["barnamy_text_chat"].get_buffer()
            widget.emit_stop_by_name("key-press-event")
            text_buffer = widget.get_buffer()
            start_sel = text_buffer.get_start_iter()
            end_sel = text_buffer.get_end_iter()
            end_chat_sel = chat_buffer.get_end_iter()
            msg = text_buffer.get_text(start_sel, end_sel, False)
            if not msg:
                return
            if msg == '/help' :
                chat_buffer.insert_with_tags(end_chat_sel, "---CMD---\n", self.join_left_cmd_tag)
                for cmd, info in self.BarnamyBase.barnamy_cmd.items():
                    end_chat_sel = chat_buffer.get_end_iter()
                    chat_buffer.insert_with_tags(end_chat_sel, "\t%s : %s\n"%(cmd, info), self.join_left_cmd_tag)

                text_buffer.set_text("")
                return
            if msg == '/run_srv':
                self.start_web_server()
                chat_buffer.insert_with_tags(end_chat_sel, "---Web server started---\n", self.join_left_cmd_tag)
                text_buffer.set_text("")                
                return

            if msg == '/stop_srv':
                self.stop_web_server()
                chat_buffer.insert_with_tags(end_chat_sel, "---Web server stoped---\n", self.join_left_cmd_tag)
                text_buffer.set_text("")                
                return

            if msg.split(' ')[0] == "/ignore" and msg.split(' ')[1]:
                self.BarnamyBase.barnamy_actions['ignore_user'](msg.split(' ')[1])
                text_buffer.set_text("")
                return

            if msg.split(' ')[0] == "/unignore" and msg.split(' ')[1]:
                self.BarnamyBase.barnamy_actions['unignore_user'](msg.split(' ')[1])
                text_buffer.set_text("")
                return

            if msg.split(' ')[0] == "/admin" and msg.split(' ')[1]:
                chat_buffer.insert_with_tags(end_chat_sel, "---Msg sent to admin---\n", self.join_left_cmd_tag)
                text_buffer.set_text("")
                data = {"type":"admin", "nick":self.nick, "token_id":self.token_id, "msg":msg}
                self.BarnamyBase.barnamy_actions['send_pub_msg'](data)
                return

            msg_lines = msg.split("\n")

            if len(msg_lines) > 7:
                self.pastebin_barnamy(msg, widget)
            else:
                data = {"type":"public", "nick":self.nick, "token_id":self.token_id, "msg":msg}
                self.BarnamyBase.barnamy_actions['send_pub_msg'](data)
                if self.EmoticonsFilter(msg):
                    msg = self.EmoticonsFilter(msg)
                self.smart_barnamy_msg(chat_buffer, msg)
                text_buffer.set_text("")
            return True
        return False

    def smart_barnamy_msg(self, chat_buffer, msg, prv = False): #I use this function just for sending public and prv msg
        for line in msg.split('\n'):
            end_iter = chat_buffer.get_end_iter()
            chat_buffer.insert(end_iter, "[%s] "%(strftime("%H:%M:%S", gmtime())))
            end_iter = chat_buffer.get_end_iter()
            if not prv:
                chat_buffer.insert_with_tags(end_iter, "<%s> "%self.nick, self.user_tag)
            else:
                self.current_user = chat_buffer.create_tag(None, foreground='blue')
                chat_buffer.insert_with_tags(end_iter, "<%s> "%self.nick, self.current_user)

            for word in line.split(" "):
                p = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
                end_iter = chat_buffer.get_end_iter()
                if p.match(word):
                    if word == line.split(" ")[-1]:self.insert_link(chat_buffer, end_iter, "%s" %word)
                    else:
                        self.insert_link(chat_buffer, end_iter, "%s" %word)
                        end_iter = chat_buffer.get_end_iter()
                        chat_buffer.insert(end_iter, " ")
                else:
                    if not prv:
                        if word == line.split(" ")[-1]:chat_buffer.insert_with_tags(end_iter, "%s" %word, self.bold)
                        else: chat_buffer.insert_with_tags(end_iter, "%s " %word, self.bold)
                    else:
                        if word == line.split(" ")[-1]:chat_buffer.insert(end_iter, "%s" %word)
                        else: chat_buffer.insert(end_iter, "%s " %word)
            chat_buffer.insert(end_iter, "\n")

    def send_prv_msg(self, widget, event):
        keyval = event.keyval
        name = Gdk.keyval_name(keyval)
        mod = Gtk.accelerator_get_label(keyval, event.state)
        if mod == "Ctrl+Mod2+Return":
            pass
        elif event.keyval == 65293:
            widget.emit_stop_by_name("key-press-event")
            text_buffer = widget.get_buffer()
            start_sel = text_buffer.get_start_iter()
            end_sel = text_buffer.get_end_iter()
            msg = text_buffer.get_text(start_sel, end_sel, False)
            if not msg:
                return
            msg_lines = msg.split("\n")
            if len(msg_lines) > 5:
                self.pastebin_barnamy(msg, text_buffer)
            else:

                chat_buffer = self.barnamy_widget_prv_chat[self.selected_prv_chat]["chat_view"].get_buffer()

                data = {"type":"private", "from_" : self.nick, "to_" : self.selected_prv_chat, "token_id" :  self.token_id, "msg" : msg}
                self.BarnamyBase.barnamy_actions['send_prv_msg'](data)
                if self.EmoticonsFilter(msg):
                    msg = self.EmoticonsFilter(msg)

                self.smart_barnamy_msg(chat_buffer, msg, True)

                text_buffer.set_text("")                
            return True
        return False

    def RunBarnamySingleChat(self, widget=None):
        if not self.build_single_chat():
            self.barnamy_widget["singleChat"].show_all()
            
        if not self.selected_user in self.barnamy_widget_prv_chat:
            paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
            paned.set_position(500)
            scrolledwindow_top = Gtk.ScrolledWindow()
            scrolledwindow_top.set_hexpand(True)
            scrolledwindow_top.set_vexpand(True)

            scrolledwindow_bottom = Gtk.ScrolledWindow()
            scrolledwindow_bottom.set_hexpand(True)
            scrolledwindow_bottom.set_vexpand(True)
            self.barnamy_widget_prv_chat[self.selected_user] = {}
            
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"] = self.ObjectGui("TextView")
            self.barnamy_widget_prv_chat[self.selected_user]["enter_view"] = self.ObjectGui("TextView")
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"] = self.ObjectGui("TextView")
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"].set_editable(False)
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"].set_cursor_visible(False)
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"].set_wrap_mode(Gtk.WrapMode.WORD)
            fontdesc = Pango.FontDescription("monospace 10.5")
            self.barnamy_widget_prv_chat[self.selected_user]["chat_view"].modify_font(fontdesc)
            
            self.barnamy_widget_prv_chat[self.selected_user]["enter_view"].connect('key-press-event', self.send_prv_msg)
            
            scrolledwindow_top.add(self.barnamy_widget_prv_chat[self.selected_user]["chat_view"])
            scrolledwindow_bottom.add(self.barnamy_widget_prv_chat[self.selected_user]["enter_view"])
            paned.pack1(scrolledwindow_top, True, False)
            paned.pack2(scrolledwindow_bottom, True, False)
            user_nick = self.ObjectGui("Label", self.selected_user)
            self.barnamy_widget["group_users"].append_page(paned, user_nick)
            self.barnamy_widget["group_users"].set_scrollable(True)
            self.barnamy_widget["group_users"].show_all()
            self.barnamy_widget_prv_chat[self.selected_user]["enter_view"].grab_focus()

    def get_user_win_prv_title(self, notebook, page, page_num):
        self.selected_prv_chat = notebook.get_tab_label(page).get_children()
        self.selected_prv_chat = self.selected_prv_chat[0].get_text()
        self.barnamy_widget["singleChat"].set_title("CONNECTED AS [%s] ### PRIVATE CHAT WITH [%s]" %(self.nick, self.selected_prv_chat))

    def do_login(self, button):
        data = {"type":"login", "nick":self.barnamy_widget["barnamy_nick_enter"].get_text(), 
                "passwd":self.barnamy_widget["barnamy_passwd_enter"].get_text()}
        self.BarnamyBase.barnamy_actions['do_login'](data)
        
        self.barnamy_widget["online_item"].show()
        self.barnamy_widget["away_status"].show()
        self.barnamy_widget["status_disconnect"].show()

    def do_login_enter_press(self, widget, event):
        if  event.keyval == 65293:
            data = {"type":"login", "nick":self.barnamy_widget["barnamy_nick_enter"].get_text(), 
                "passwd":self.barnamy_widget["barnamy_passwd_enter"].get_text()}
            self.barnamy_widget["online_item"].show()
            self.barnamy_widget["away_status"].show()
            self.barnamy_widget["status_disconnect"].show()
            self.BarnamyBase.barnamy_actions['do_login'](data)

    def do_logout(self, button):
        data = {'type' : 'logout', 'nick' : self.nick, 'token_id' : self.token_id}
        self.BarnamyBase.barnamy_actions['do_logout'](data)
        self.BarnamyBase.barnamy_actions['stop_web_server']()

        self.RunBarnamyLogin()
        self.HideBarnamyChat()
        barnamy_tag_table = self.textbuffer.get_tag_table()
        for user in self.color_dic:
            tag = barnamy_tag_table.lookup(user)
            barnamy_tag_table.remove(tag)
        self.color_dic.clear()
        self.nick = None
        self.token_id = None
        self.selected_user = None
        self.barnamy_widget["status_disconnect"].hide()
        self.barnamy_widget["online_item"].hide()
        self.barnamy_widget["away_status"].hide()
        self.hide_private_chat()

    def on_user_list_button_press_event(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.barnamy_widget["user_menu"].popup(None, None, None, None, event.button, time)
            return True
    
    def on_user_list_double_click(self, treeview, event):
        if event.button == 1:
            data = treeview.get_path_at_pos(int(event.x), int(event.y))
            if data :
                if event.type == self.ObjectGui("double_click"):
                    self.RunBarnamySingleChat()

    def on_selected_user_change(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.selected_user = value

    def search_user_to_change_status(self, p_user, status):

        for users in self.user_liststore:
            if users[0] == p_user:
                if status == "Away": users[1] = "Away"
                else: users[1] = "Online"
        
        return False

    def status_online(self, widget):
        self.search_user_to_change_status(self.nick, "online")
        data = {'type':'status', 'nick':self.nick, 'status':'Online', 'token_id':self.token_id}
        self.BarnamyBase.barnamy_status['online'](data)

    def status_away(self, widget):
        self.search_user_to_change_status(self.nick, "Away")
        data = {'type':'status', 'nick':self.nick, 'status':'Away', 'token_id':self.token_id}
        self.BarnamyBase.barnamy_status['away'](data)

    def ask_to_access_forlder(self, wiget):
        data = {'type':'folder', 'from_':self.nick, 'to_':self.selected_user, 'token_id':self.token_id}
        self.BarnamyBase.barnamy_actions['ask_for_folder_access'](data)

    def back(self, wiget):
        if self.position - 1 != -1:
            self.position -= 1
            self.barnamy_widget["l_count"].set_text("%d/%d"%(self.position +1, len(self.users_access)))
            self.barnamy_widget["user_nick"].set_markup("<b>%s</b> sends a request private folder access" %self.users_access[self.position])

    def forward(self, wiget):
        if len(self.users_access) - 1 > self.position:
            self.position += 1
            self.barnamy_widget["l_count"].set_text("%d/%d"%(self.position + 1, len(self.users_access)))
            self.barnamy_widget["user_nick"].set_markup("<b>%s</b> sends a request private folder access" %self.users_access[self.position])

    def accept(self, wiget):
        self.BarnamyBase.barnamy_actions['accept_share'](self.users_access[self.position])
        self.users_access.pop(self.position)
        if len(self.users_access) == 0:
            self.HideAccessOrder()
        else:
            self.position -=1
            if self.position == -1:
                self.position = 0
            self.barnamy_widget["l_count"].set_text("%d/%d"%(self.position + 1, len(self.users_access)))
            self.barnamy_widget["user_nick"].set_markup("<b>%s</b> sends a request private folder access" %self.users_access[self.position])

    def cancel(self, wiget):
        self.users_access.pop(self.position)
        if len(self.users_access) == 0:
            self.HideAccessOrder()
        else:
            self.position -=1
            if self.position == -1:
                self.position = 0
            self.barnamy_widget["l_count"].set_text("%d/%d"%(self.position + 1, len(self.users_access)))
            self.barnamy_widget["user_nick"].set_markup("<b>%s</b> sends a request private folder access" %self.users_access[self.position])

    def barnamy_settings_open(self, widget = 0, event=0):
        self.barnamy_widget["baramy_settings"].show_all()

        settings = self.BarnamyBase.barnamy_settings_actions['get_settings']()
        self.barnamy_widget['entry_ip'].set_text(settings['ip'])
        self.barnamy_widget['entry_port'].set_text(str(settings['port']))
        self.barnamy_widget['entry_wport'].set_text(str(settings['wport']))
        self.barnamy_widget['switch_sound'].set_active(settings['sound'])
        self.barnamy_widget['switch_notify'].set_active(settings['notify'])
        self.barnamy_widget['switch_log'].set_active(settings['log'])
        self.barnamy_widget["switch_tls"].set_active(settings['tls'])

    def barnamy_settings_close(self, widget = 0, event = 0):
        self.barnamy_widget["baramy_settings"].hide()
        if not self.pre_login and not self.post_login:
            self.stop()
        return True

    def barnamy_save_setting(self, widget):
        settings = {"ip":self.barnamy_widget["entry_ip"].get_text(), "port":self.barnamy_widget["entry_port"].get_text(), "wport":self.barnamy_widget["entry_wport"].get_text(),
                    "sound":self.barnamy_widget["switch_sound"].get_active(), "notify":self.barnamy_widget["switch_notify"].get_active(),
                    "log":self.barnamy_widget["switch_log"].get_active(), "tls":self.barnamy_widget["switch_tls"].get_active()}

        self.BarnamyBase.barnamy_settings_actions['save_settings'](settings)
        return True

    def hide_about_barnamy(self, widget = 0, event = 0):
        self.barnamy_widget['aboutBarnamy'].hide()
        return True

    def focus_in_private_chat(self, widget, event):
        self.hint_prv = False
        self.barnamy_widget['singleChat'].set_urgency_hint(self.hint_prv)

    def focus_in_public_chat(self, widget, event):
        self.hint_public = False
        self.barnamy_widget['barnamy_chat_window'].set_urgency_hint(self.hint_public)

    def focus_out_private_chat(self, widget, event):
        self.hint_prv = True

    def focus_out_public_chat(self, widget, event):
        self.hint_public = True

    def insert_link(self, buffer, iter, url):
        tag = buffer.create_tag(None, underline=Pango.Underline.SINGLE, foreground ="blue")
        tag.set_property("underline",Pango.Underline.SINGLE)
        buffer.insert_with_tags(iter, url, tag)
        tag.connect("event", self.open_link, url)

    def open_link(self, rr, tt, yy, qq, url):
        if yy.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            webbrowser.open(url, new=0, autoraise=True)

    def motion_notify_event(self, widget, event):
        x, y = widget.window_to_buffer_coords(Gtk.TextWindowType.TEXT, event.x, event.y)
        self.set_cursor_if_appropriate (widget, x, y);
        return False

    def set_cursor_if_appropriate(self, widget, x, y):
        tags = None
        hovering = False
        iter = widget.get_iter_at_location (x, y)
        tags = iter.get_tags();
        for tag in tags:
            value = tag.get_property("underline")
            if value:
                hovering = True
                break

        if hovering != self.hovering_over_link:
            self.hovering_over_link = hovering

            if self.hovering_over_link:
                link = Gdk.Cursor(Gdk.CursorType.HAND2)
                gdk_window = widget.get_window(Gtk.TextWindowType.TEXT)
                gdk_window.set_cursor(link)
            else:
                test = Gdk.Cursor(Gdk.CursorType.XTERM)
                gdk_window = widget.get_window(Gtk.TextWindowType.TEXT)
                gdk_window.set_cursor(test)

        if tags:
            tags = None

