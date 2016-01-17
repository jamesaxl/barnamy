# -*- coding: utf-8 -*-

import sys, os, pygtk
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import Gst
GObject.threads_init()
Gst.init(None)

class BarnamyAudio(object):
    def __init__(self):
        Gst.init_check(None)
        self.IS_GST010 = Gst.version()[0] == 0
        self.player = Gst.ElementFactory.make('playbin', None)
    
    def _play_file(self, file_s):
        self.player.set_state(Gst.State.NULL)
        self.player.set_property('uri', file_s)
        self.player.set_state(Gst.State.PLAYING)

    def login_sound(self):
        self._play_file('file://'+os.path.abspath('Sound/service-login.ogg'))
    
    def logout_sound(self):
        self._play_file('file://'+os.path.abspath('Sound/service-logout.ogg'))

    def send_msg_sound(self):
        self._play_file('file://'+os.path.abspath('Sound/send.ogg'))

    def receive_msg_sound(self):
        self._play_file('file://'+os.path.abspath('Sound/receive.ogg'))
    
    def access_folder_sound(self):
        self._play_file('file://'+os.path.abspath('Sound/folder_access.ogg'))
