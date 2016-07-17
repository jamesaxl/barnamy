# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:33:52 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from time import gmtime, strftime
import re
import random

class BarnamyChatViewer(Gtk.TextView):
    def __init__(self):
        Gtk.TextView.__init__(self)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        self.modify_font(Pango.FontDescription("monospace 10.5"))
        self.chat_buffer = self.get_buffer()
        self.highlight_tag = self.chat_buffer.create_tag("hight", foreground="#FF0000")
        self.user_tag = self.chat_buffer.create_tag("user_color", foreground="#0000FF")
        self.join_left_cmd_tag = self.chat_buffer.create_tag("join_left", foreground="#999999")
        self.users_tag = {}
        self.bold = self.chat_buffer.create_tag( "bold", weight=Pango.Weight.BOLD)

    def put_msg_(self, nick, msg):
        
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        end_chat_sel = self.chat_buffer.get_end_iter()
        
        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S", gmtime()),))
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.user_tag, self.bold)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '%s\n' %msg, self.bold)

    def radom_color(self, nick):
        colors = ['#FF0000', '#FF0088', '#FF00FF', '#8400FF', 
        '#0084FF', '#00FF84', '#00FF00', '#FF8000', '#008800']
        return self.chat_buffer.create_tag(nick, foreground=random.choice(colors))

    def rcev_msg(self, nick, msg):
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S", gmtime()),))
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.users_tag[nick], self.bold)

        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '%s\n' %msg, self.bold)

    def rcev_msg_highlight(self, nick, msg):
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S", gmtime()),))
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.highlight_tag, self.bold)

        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '%s\n' %msg, self.highlight_tag, self.bold)

    def recv_prv_msg(self, nick, msg):
        if self.emoticons_filter(msg):
            msg = self.emoticons_filter(msg)
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "[%s]"%(strftime("%H:%M:%S", gmtime()),))
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '<%s> ' %nick, 
                                     self.users_tag[nick], self.bold)

        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, '%s\n' %msg, self.bold)

    def put_help_(self, cmds):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "---CMD---\n", self.join_left_cmd_tag)
        for cmd, info in cmds.items():
            end_chat_sel = self.chat_buffer.get_end_iter()
            self.chat_buffer.insert_with_tags(end_chat_sel, "\t%s : %s\n"%(cmd, info), self.join_left_cmd_tag)


    def put_folder_access(self, user):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "##### You receive a request from %s for sharing folder. To allow this user please type /allow <nick> #####\n"%user,
                                          self.join_left_cmd_tag)

    def put_folder_access_valid(self, nick, passwd):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "---%s accepted you, the Password is %s and you should not lose it---\n"%(nick, passwd), 
            self.join_left_cmd_tag)

    def recv_left_joing(self, msg):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert_with_tags(end_chat_sel, "[%s] %s\n" %(strftime("%H:%M:%S", gmtime()), msg,), self.join_left_cmd_tag)

    def barnamy_welcome(self):
        end_chat_sel = self.chat_buffer.get_end_iter()
        self.chat_buffer.insert(end_chat_sel, "   BBBBBBBBBBBBBBBBB\n")
        self.chat_buffer.insert(end_chat_sel, "   B::::::::::::::::B \n")
        self.chat_buffer.insert(end_chat_sel, "   B::::::BBBBBB:::::B\n")
        self.chat_buffer.insert(end_chat_sel, "   BB:::::B     B:::::B \n")
        self.chat_buffer.insert(end_chat_sel, "     B::::B     B:::::B  aaaaaaaaaaaaa  rrrrr   rrrrrrrrr   nnnn  nnnnnnnn      aaaaaaaaaaaaa      mmmmmmm    mmmmmmm yyyyyyy           yyyyyyy\n")
        self.chat_buffer.insert(end_chat_sel, "     B::::B     B:::::B  a::::::::::::a r::::rrr:::::::::r  n:::nn::::::::nn  a::::::::::::a   mm:::::::m  m:::::::mmy:::::y           y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "     B::::BBBBBB:::::B   aaaaaaaaa:::::ar:::::::::::::::::r n::::::::::::::nn   aaaaaaaaa:::::a m::::::::::mm::::::::::my:::::y       y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "     B:::::::::::::BB             a::::arr::::::rrrrr::::::rnn:::::::::::::::n           a::::a m::::::::::::::::::::::m y:::::y     y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "     B::::BBBBBB:::::B     aaaaaaa:::::a r:::::r     r:::::r  n:::::nnnn:::::n    aaaaaaa:::::a m:::::mmm::::::mmm:::::m  y:::::y   y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "     B::::B     B:::::B  aa::::::::::::a r:::::r     rrrrrrr  n::::n    n::::n  aa::::::::::::a m::::m   m::::m   m::::m   y:::::y y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "     B::::B     B:::::B a::::aaaa::::::a r:::::r              n::::n    n::::n a::::aaaa::::::a m::::m   m::::m   m::::m    y:::::y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "     B::::B     B:::::Ba::::a    a:::::a r:::::r              n::::n    n::::na::::a    a:::::a m::::m   m::::m   m::::m     y:::::::::y  \n")
        self.chat_buffer.insert(end_chat_sel, "   BB:::::BBBBBB::::::Ba::::a    a:::::a r:::::r              n::::n    n::::na::::a    a:::::a m::::m   m::::m   m::::m      y:::::::y \n")
        self.chat_buffer.insert(end_chat_sel, "   B:::::::::::::::::B a:::::aaaa::::::a r:::::r              n::::n    n::::na:::::aaaa::::::a m::::m   m::::m   m::::m       y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "   B::::::::::::::::B   a::::::::::aa:::ar:::::r              n::::n    n::::n a::::::::::aa:::am::::m   m::::m   m::::m      y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "   BBBBBBBBBBBBBBBBB     aaaaaaaaaa  aaaarrrrrrr              nnnnnn    nnnnnn  aaaaaaaaaa  aaaammmmmm   mmmmmm   mmmmmm     y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "                                                                                                                            y:::::y \n")
        self.chat_buffer.insert(end_chat_sel, "                                                                                                                           y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "                                                                                                                          y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "                                                                                                                         y:::::y\n")
        self.chat_buffer.insert(end_chat_sel, "                                                                                                                        yyyyyyy\n")
        self.chat_buffer.insert(end_chat_sel, "\n")
        self.chat_buffer.insert(end_chat_sel, "\n")

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
