# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:50:04 2016

@author: jamesaxl
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from BarnamyPrivateChat import BarnamyPrivateChat
from BarnamyPrivateChat import USERS_CHAT
from BarnamyChatViewer import BarnamyChatViewer


class BarnamyUserList(Gtk.TreeView):

    def __init__(self, Base):
        Gtk.TreeView.__init__(self)
        self.BarnamyBase = Base
        self.user_liststore = Gtk.ListStore(str, str)
        users_rend = Gtk.CellRendererText()
        status_rend = Gtk.CellRendererText()
        users_col = Gtk.TreeViewColumn("Users", users_rend, text=0)
        status_col = Gtk.TreeViewColumn("Status", status_rend, text=1)
        self.append_column(users_col)
        self.append_column(status_col)
        self.set_model(self.user_liststore)
        self.connect('button_press_event', self.on_user_list_button_press_event)
        self.connect('button_press_event', self.on_user_list_double_click)
        self.get_selection().connect("changed", self.on_selected_user_change)
        self.selected_prv_chat = None
        self.barnamy_private_win = BarnamyPrivateChat(self.BarnamyBase)
        self.users_tab = self.barnamy_private_win.users_tab
        self.users_tab.connect('switch-page', self.get_user_win_prv_title)
        self.menu = Gtk.Menu()
        prv_chat = Gtk.MenuItem("Private chat")
        fldr_access = Gtk.MenuItem("Folder Access")
        prv_chat.connect('activate', self.on_private_chat_clicked)
        fldr_access.connect('activate', self.on_fldr_access_clicked)
        self.menu.append(prv_chat)
        self.menu.append(fldr_access)
        prv_chat.show()
        fldr_access.show()

    def on_selected_user_change(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.selected_user = value

    def on_user_list_double_click(self, treeview, event):
        if event.button == 1:
            data = treeview.get_path_at_pos(int(event.x), int(event.y))
            if data :
                if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
                    self.private_chat(self.selected_user)

    def on_private_chat_clicked(self, widget):
        self.private_chat(self.selected_user)

    def on_fldr_access_clicked(self, widget):
        data = {'type':'folder', 'from_':self.BarnamyBase.nick[0], 'to_':self.selected_user, 'token_id':self.BarnamyBase.token_id[0]}
        self.BarnamyBase.barnamy_actions['ask_for_folder_access'](data)

    def private_chat(self, nick):
        if nick in USERS_CHAT:
            return
        USERS_CHAT[nick] = {'chat_private_view' : BarnamyChatViewer(), 
                                'entry_text' : Gtk.Entry()}
        USERS_CHAT[nick]['chat_private_view'].users_tag[nick] = USERS_CHAT[nick]['chat_private_view'].radom_color(nick)
        if not self.BarnamyBase.nick[0] in USERS_CHAT[nick]['chat_private_view'].users_tag:
            USERS_CHAT[nick]['chat_private_view'].users_tag[self.BarnamyBase.nick[0]] = USERS_CHAT[nick]['chat_private_view'].chat_buffer.create_tag("user_color", foreground="#0000FF")
        chat_view_scrollbar = Gtk.ScrolledWindow()
        chat_view_scrollbar.add(USERS_CHAT[nick]['chat_private_view'])
        main_chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=7)
        main_chat_box.set_border_width(7)
        main_chat_box.pack_start(chat_view_scrollbar, True, True, 0)
        main_chat_box.pack_start(USERS_CHAT[nick]['entry_text'], False, True, 0)
        label = Gtk.Label(label="%s" %str(nick))
        button = Gtk.Button("X")
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button.connect('clicked', self.on_closetab_button_clicked, hbox)
        USERS_CHAT[nick]['entry_text'].connect('key-press-event', self.send_prv_msg)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(button, False, False, 0)
        hbox.show_all()
        self.users_tab.append_page(main_chat_box, hbox)
        self.barnamy_private_win.show_all()
        USERS_CHAT[nick]['entry_text'].grab_focus()

    def on_closetab_button_clicked(self, sender, widget):

        nick = widget.get_children()[0].get_text()
        #pagenum = self.users_tab.page_num(widget)
        page_num = self.users_tab.get_current_page()   
        if self.users_tab.get_n_pages() == 1:
            self.barnamy_private_win.hide()        
        self.users_tab.remove_page(page_num)
        del USERS_CHAT[nick]

    def send_prv_msg(self, widget, event):
        if event.keyval == 65293:
            widget.emit_stop_by_name("key-press-event")
            msg = widget.get_text()
            widget.set_text('')
            nick = self.selected_prv_chat
            USERS_CHAT[nick]['chat_private_view'].put_msg_(self.BarnamyBase.nick[0], msg)
         
            data = {'type' : 'private', 'to_' : nick, 'from_' : self.BarnamyBase.nick[0], 
            'token_id' : self.BarnamyBase.token_id[0], 'msg' : msg}
            self.BarnamyBase.barnamy_actions['send_prv_msg'](data)

    def recv_prv_msg(self, data):
        self.private_chat(data['from_'])
        USERS_CHAT[data['from_']]['chat_private_view'].recv_prv_msg(data['from_'], data['msg'])
        self.barnamy_private_win.set_urgency_hint(True)


    def recv_user_join_left_prv(self, data):
        if data['user'] in USERS_CHAT:
            USERS_CHAT[data['user']]['chat_private_view'].recv_left_joing(data['user_join_left'])
            if data['user'] in data['user_list']:
                USERS_CHAT[data['user']]['entry_text'].set_sensitive(True)
            else:
                USERS_CHAT[data['user']]['entry_text'].set_sensitive(False)

    def update_users_list(self, nick):
        for user in self.user_liststore:
            if user[0] == nick:
                self.user_liststore.remove(user.iter)
                return
        self.user_liststore.append([nick, "Online"])
        

    def get_user_win_prv_title(self, notebook, page, page_num):
        self.selected_prv_chat = notebook.get_tab_label(page).get_children()
        self.selected_prv_chat = self.selected_prv_chat[0].get_text()
        self.barnamy_private_win.set_title("CONNECTED AS [%s] ### PRIVATE CHAT WITH [%s]" %(self.BarnamyBase.nick[0], self.selected_prv_chat))

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
                
                self.menu.popup(None, None, None, None, event.button, time)
            return True
