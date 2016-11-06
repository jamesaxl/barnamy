# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:33:52 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk
from time import strftime
import webbrowser
import re
import random

class BarnamyChatViewer(Gtk.TextView):
    def __init__(self):
        Gtk.TextView.__init__(self)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        self.modify_font(Pango.FontDescription("monospace 10.5"))
        self.connect('motion-notify-event', self.motion_notify_event)
        self.chat_buffer = self.get_buffer()
        self.highlight_tag = self.chat_buffer.create_tag("hight", foreground="#FF0000")
        self.join_left_cmd_tag = self.chat_buffer.create_tag("join_left", foreground="#999999")
        self.tag_url = self.chat_buffer.create_tag(None, underline=Pango.Underline.SINGLE, foreground ="blue")
        self.tag_url.set_property("underline",Pango.Underline.SINGLE)
        self.users_tag = {}
        self.bold = self.chat_buffer.create_tag( "bold", weight=Pango.Weight.BOLD)
        self.hovering_over_link = False

    def put_msg_(self, nick, msg):
        
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        
        end_chat_sel = self.chat_buffer.get_end_iter()

        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S"),))
        end_chat_sel = self.chat_buffer.get_end_iter()

        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.users_tag[nick], self.bold)
        
        end_chat_sel = self.chat_buffer.get_end_iter()            
        self.chat_buffer.insert_with_tags(end_chat_sel, msg, self.bold)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "\n")
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)
        msg = msg.split(' ')
        url_reg = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        for word in msg:
            if url_reg.match(word):
                start = self.chat_buffer.get_start_iter()
                self.search_link_and_tag(word, start)
        #self.BarnamyBase.

    def search_link_and_tag(self, word, start):
        end_chat_sel = self.chat_buffer.get_end_iter()
        found_link_word = start.forward_search(word, Gtk.TextSearchFlags.TEXT_ONLY, end_chat_sel)
        if found_link_word:
            match_start, match_end  = found_link_word
            self.chat_buffer.apply_tag(self.tag_url, match_start, match_end)
            self.tag_url.connect("event", self.open_link, word)
            self.search_link_and_tag(word, match_end)
        

    def radom_color(self, nick):
        colors = ['#FF0000', '#FF0088', '#FF00FF', '#8400FF', 
        '#0084FF', '#00FF84', '#00FF00', '#FF8000', '#008800']
        return self.chat_buffer.create_tag(nick, foreground=random.choice(colors))

    def rcev_msg(self, nick, msg):
        self.put_msg_(nick, msg)

    def rcev_msg_highlight(self, nick, msg):
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S"),))
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.highlight_tag, self.bold)

        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '%s\n' %msg, self.highlight_tag, self.bold)

    def recv_prv_msg(self, nick, msg):
        self.put_msg_(nick, msg)

    def put_help_(self, cmds):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "---CMD---\n", self.join_left_cmd_tag)
        for cmd, info in cmds.items():
            end_chat_sel = self.chat_buffer.get_end_iter()
            self.chat_buffer.insert_with_tags(end_chat_sel, "\t%s : %s\n"%(cmd, info), self.join_left_cmd_tag)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)


    def put_folder_access(self, user):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "##### You receive a request from %s for sharing folder. To allow this user please type /allow <nick> #####\n"%user,
                                          self.join_left_cmd_tag)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def put_folder_access_valid(self, nick, passwd):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "---%s is accepted you, the Password is %s and you should not lose it---\n"%(nick, passwd), 
            self.join_left_cmd_tag)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def recv_left_joing(self, msg):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "[%s] %s\n" %(strftime("%H:%M:%S"), msg,), self.join_left_cmd_tag)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def put_user_info(self, nick, info):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "\n-- Nick = > %s | Host => %s --\n" %(nick, info), self.join_left_cmd_tag, self.bold)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def barnamy_welcome(self):
        end_chat_sel = self.chat_buffer.get_end_iter()
        barnamy_welcome = "-- Welcome to Barnamy world, please enjoy and do not cross your limit :-) --\n"
        barnamy_welcome = self.emoticons_filter(barnamy_welcome)
        self.chat_buffer.insert(end_chat_sel, barnamy_welcome)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def put_barnamy_quote(self, quote):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "\n[%s] said: [%s]\n"%(quote.keys()[0], quote[quote.keys()[0]]), self.join_left_cmd_tag, self.bold)
        self.scroll_to_mark(self.chat_buffer.get_insert(), 0.0, True, 0.5, 0.5)

    def unicode_emoticons_list(self, emoticon):
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

    def emoticons_filter(self, msg):
        filter = re.findall(":-\)|:D|3:\)|o:\)|:\(|:p", msg)
        if filter:
            for i in filter:
                msg = msg.replace(i, self.unicode_emoticons_list(i))
            return msg
        return False

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
