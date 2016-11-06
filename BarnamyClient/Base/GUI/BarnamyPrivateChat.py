# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 18:24:36 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

from BarnamySettingsGui import BarnamySettingsGui
from BarnamyNewUser import BarnamyNewUser
from BarnamyChatViewer import BarnamyChatViewer

USERS_CHAT = {}

class BarnamyPrivateChat(Gtk.ApplicationWindow):
    def __init__(self, Base):
        if Base:
            self.BarnamyBase = Base

        Gtk.Window.__init__(self) 
        self.users_tab = Gtk.Notebook()
        self.add(self.users_tab)
        self.resize(800, 600)
        self.connect('delete-event', self.hide_private_chat)
        self.connect('focus-in-event', self.lost_hint)


    def lost_hint(self, widget, event):
        self.set_urgency_hint(False)

    def hide_private_chat(self, widget = 0, event = 0):
        for page in range(0, self.users_tab.get_n_pages()):
            self.users_tab.remove_page(0)
        USERS_CHAT.clear()
        self.hide()
        return True
        