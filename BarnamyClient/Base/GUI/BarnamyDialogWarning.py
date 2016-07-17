# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:05:52 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BarnamyDialogWarning(object):

    def __init__(self, parent, text):
        dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Barnamy Warning")
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

class BarnamyDialogAbout(object):
    
    def __init__(self, parent):
        self._builder = Gtk.Builder()
        self.barnamy_widget = {}
        self._builder.add_from_file("Theme/GuiGtk/barnamy_about.glade")
        self.barnamy_widget["about_barnamy"] = self._builder.get_object("about_barnamy")
        self.barnamy_widget["about_barnamy"].set_transient_for(parent)
        self.barnamy_widget["aboutdialog-action_area"] = self._builder.get_object("aboutdialog-action_area")
        self.barnamy_widget["about_barnamy"].connect('delete-event', self.close)
        self.barnamy_widget["aboutdialog-action_area"].get_children()[2].connect('clicked', self.close)
        

    def run(self):
        self.barnamy_widget["about_barnamy"].show_all()

    def close(self, widget):
        self.barnamy_widget["about_barnamy"].hide()