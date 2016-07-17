# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:09:58 2016

@author: jamesaxl
"""
import gi
gi.require_version('Gtk', '3.0')
from twisted.internet import gtk3reactor
gtk3reactor.install()

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GdkPixbuf

from twisted.internet import reactor
from time import gmtime, strftime
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
from BarnamySettingsGui import BarnamySettingsGui
from BarnamyNewUser import BarnamyNewUser
from BarnamyChatWindow import BarnamyChatWindow
from BarnamyDialogWarning import BarnamyDialogWarning
from BarnamyDialogWarning import BarnamyDialogAbout

class BarnamyLogin(Gtk.ApplicationWindow):

    def __init__(self, Base = 0):
        self.BarnamyBase = Base
        
        Gtk.Window.__init__(self, title="Barnamy Login")
        self.statusbar = Gtk.Statusbar()        
        self.set_default_size(400, 300)
        self.barnamy_pixbuf = GdkPixbuf.Pixbuf.new_from_file("Theme/GuiGtk/B7_100x102.png")
        self.set_icon(self.barnamy_pixbuf)
        self.connect("delete-event", Gtk.main_quit)
        self.connect("delete-event", self.barnamy_close)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Barnamy Login"
        self.set_titlebar(hb)

        barnamy_login_button_menu = Gtk.MenuButton()
        barnamy_login_button_menu.set_size_request(80, 35)
        hb.pack_start(barnamy_login_button_menu)
        menumodel = Gio.Menu()
        menumodel.append("New User", "win.new")
        menumodel.append("Settings", "win.settings")
        menumodel.append("About", "win.about")
        menumodel.append("Quit", "win.quit")

        self.settings_ins = BarnamySettingsGui(self.BarnamyBase)
        self.barnamy_new_user_ins = BarnamyNewUser(self.BarnamyBase)
        self.recv_register = self.barnamy_new_user_ins.recv_register

        barnamy_login_button_menu.set_menu_model(menumodel)
        
        new_user_action = Gio.SimpleAction.new("new", None)
        new_user_action.connect("activate", self.barnamy_new_user)
        self.add_action(new_user_action)
        
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.barnamy_close)
        self.add_action(quit_action)
        
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.barnamy_settings)
        self.add_action(settings_action)

        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        
        self.barnamy_login_entry = Gtk.Entry()
        self.barnamy_password_entry = Gtk.Entry()
        self.barnamy_login_entry.set_placeholder_text('Login')
        self.barnamy_password_entry.set_placeholder_text('Password ')
        self.barnamy_password_entry.set_visibility(False)
        login_bt = Gtk.Button('Login')

        login_bt.connect('clicked', self.barnamy_login)        
        
        hbox1.pack_start(login_bt, True, False, 0)
        hbox2.pack_start(self.barnamy_login_entry, True, False, 0)
        hbox3.pack_start(self.barnamy_password_entry, True, False, 0)
        
        self.label = Gtk.Image()
        barnamy_pixbuf = GdkPixbuf.Pixbuf.new_from_file("Theme/GuiGtk/B7_100x102.png")
        self.label.set_from_pixbuf(barnamy_pixbuf)
        vbox1.pack_start(self.label, False, False, 0)
        vbox1.pack_start(hbox2, False, False, 0)
        vbox2.pack_start(hbox3, False, False, 0)
        vbox2.pack_start(hbox1, False, True, 0)
        vbox1.pack_start(vbox2, False, False, 0)
        vbox1.pack_end(self.statusbar, False, True, 0)

        vbox1.set_border_width(10)
        self.add(vbox1)
        
        self.barnamy_chat_window_ins = None
        self.barnamy_login_win_state = False

    def recv_status_before_login(self, data):
        context_id = self.statusbar.get_context_id("barnamy")
        message_id = self.statusbar.push(context_id, data["status"]) 

    def about_callback(self, action, parameter):
        BarnamyDialogAbout(self).run()

    def barnamy_close(self, widget, event):
        self.stop()

    def barnamy_settings(self, action, parameter):
        self.settings_ins.barnamy_settings_open()

    def barnamy_new_user(self, action, parameter):
        self.barnamy_new_user_ins.show_all()

    def barnamy_login(self, widget):
        data = {"type":"login", "nick":self.barnamy_login_entry.get_text(), 
                "passwd":self.barnamy_password_entry.get_text()}
        self.BarnamyBase.barnamy_actions['do_login'](data)


    def recv_login_users(self, data):
        self.barnamy_chat_window_ins = BarnamyChatWindow(self.BarnamyBase, self)
        self.hide()
        for user in data['user_list']:
            if user != data['nick']:
                self.barnamy_chat_window_ins.barnamy_text_chat_view.users_tag[user] = self.barnamy_chat_window_ins.barnamy_text_chat_view.radom_color(user)

        for user in data['user_list']:
            self.barnamy_chat_window_ins.barnamy_user_list.update_users_list(user)
        self.barnamy_chat_window_ins.RunBarnamyChatWindow()
        self.barnamy_login_win_state = False

    def recv_login_nok(self, data):
        BarnamyDialogWarning(self, data['msg'])

    def recv_error_schema(self, data):
        print data
        print "For more info please contact the developer of Barnamy and do not forget to explain what you did to get this message error..."

    def RunBarnamyLogin(self):
        self.show_all()
        self.barnamy_login_win_state = True

    def stop(self, widget = 0):
        reactor.stop()
