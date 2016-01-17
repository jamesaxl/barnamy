# -*- coding: utf-8 -*-
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

class BarnamyNotify(object):

    def __init__(self):
        
        self.notify = Notify.init("BarnamyNotify")

    def show_notify(self, user, text):
        user=Notify.Notification.new(user, text, "dialog-information")
        user.show()
