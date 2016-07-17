# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 14:22:47 2016

@author: jamesaxl
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

import os

class BarnamyStatusIcon(Gtk.StatusIcon):
    def __init__(self, Base, windows_list):
        
        self.BarnamyBase = Base
        self.windows_list = windows_list
        Gtk.StatusIcon.__init__(self, title="Barnamy")
        self.set_tooltip_text("Barnamy")
        barnamy_pixbuf = GdkPixbuf.Pixbuf.new_from_file("Theme/GuiGtk/B7_25x26.png")
        self.set_from_pixbuf(barnamy_pixbuf)
        self.connect('button-press-event', self.status_press_button)

    def status_press_button(self, widget, event):
        if event.button == 1:
            if self.BarnamyBase.token_id != None:
                if self.windows_list[1].barnamy_chat_win_state: 
                    self.windows_list[1].hide()
                    self.windows_list[1].barnamy_chat_win_state = False
                else :
                    self.windows_list[1].show_all()
                    self.windows_list[1].barnamy_chat_win_state = True
            else:
                if self.windows_list[0].barnamy_login_win_state:
                    self.windows_list[0].hide()
                    self.windows_list[0].barnamy_login_win_state = False
                else:
                    self.windows_list[0].show_all()
                    self.windows_list[0].barnamy_login_win_state = True
                
        elif event.button == 3:
            print "menu show"            
            #self.barnamy_widget["status_menu"].popup(None, None, None, None, event.button, event.time)

    def logout(self):
        pass