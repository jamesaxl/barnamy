# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 19:15:14 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from BarnamyDialogWarning import BarnamyDialogWarning

import re
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class BarnamyNewUser(Gtk.ApplicationWindow):

    def __init__(self, Base):
        self.BarnamyBase = Base
        Gtk.Window.__init__(self, title="Barnamy Login")        
        self.connect("delete-event", self.barnamy_new_user_close)
        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        
        self.nickname = Gtk.Entry()
        self.nickname.set_placeholder_text('Nickname')
        self.email_ = Gtk.Entry()
        self.email_.set_placeholder_text('@')
        self.passwd = Gtk.Entry()
        self.passwd.set_visibility(False)
        self.passwd.set_placeholder_text('Password')
        self.r_passwd = Gtk.Entry()
        self.r_passwd.set_visibility(False)
        self.r_passwd.set_placeholder_text('Re-Password')
        self.statusbar = Gtk.Statusbar()
        
        save = Gtk.Button('Register')
        close = Gtk.Button('Close')
        clear = Gtk.Button('Clear')

        close.connect('clicked', self.barnamy_new_user_close)
        save.connect('clicked', self.regiser_new_user)
        clear.connect('clicked', self.clear_entry)

        vbox1.pack_start(self.nickname, False, True, 0)
        vbox1.pack_start(self.email_, False, True, 0)
        vbox1.pack_start(self.passwd, False, True, 0)
        vbox1.pack_start(self.r_passwd, False, True, 0)
        vbox1.pack_end(hbox1, False, True, 0)
        vbox1.pack_end(self.statusbar, False, True, 0)
        hbox1.pack_start(save, False, True, 0)
        hbox1.pack_end(clear, False, True, 0)
        hbox1.pack_end(close, False, True, 0)
        vbox1.set_border_width(10)
        self.add(vbox1)

    def barnamy_new_user_close(self, widget, event = 0):
        self.hide()

    def recv_register(self, data):
        context_id = self.statusbar.get_context_id("Barnamy")
        message_id = self.statusbar.push(context_id, data["succ"])
        self.clear_entry(None)

    def regiser_new_user(self, widget):
        if not self.nickname.get_text():
            BarnamyDialogWarning(self, "Nick required")
            return

        if not self.email_.get_text():
            BarnamyDialogWarning(self, "Email required")
            return


        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email_.get_text()) == None:
            BarnamyDialogWarning(self, "Email not valid")
            return

        if not self.passwd.get_text():
            BarnamyDialogWarning(self, "Password required")
            return

        if not self.r_passwd.get_text():
            BarnamyDialogWarning(self, "Password comfirmation required")
            return

        if self.passwd.get_text() != self.r_passwd.get_text():
            BarnamyDialogWarning(self, "Password and Re-password should be the same")
            return

        data = {"type":"register", "nick":self.nickname.get_text(), "email":self.email_.get_text(), 
                "passwd":self.passwd.get_text()}

        self.BarnamyBase.barnamy_actions['regiser_new_user'](data)

    def clear_entry(self, widget):
        self.nickname.set_text('')
        self.email_.set_text('')
        self.passwd.set_text('')
        self.r_passwd.set_text('')
