# -*- coding: utf-8 -*-
cache()

from zope.interface import implements
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.web.static import File
from twisted.web.resource import IResource
from twisted.web.guard import HTTPAuthSessionWrapper, DigestCredentialFactory
from os.path import expanduser
import os

BARNAMY_HTTP_PASSWD_FILE = expanduser("~/.barnamy/httpd.password")
BARNAMY_HOME = expanduser("~/BarnamyHome")
if not os.path.exists(BARNAMY_HOME):
	os.makedirs(BARNAMY_HOME)

class PublicHTMLRealm(object):
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            return (IResource, File("%s/%s/" % (BARNAMY_HOME, avatarId)), lambda: None)
        raise NotImplementedError()

portal = Portal(PublicHTMLRealm(), [FilePasswordDB(BARNAMY_HTTP_PASSWD_FILE)])

credentialFactory = DigestCredentialFactory("md5", "bflk")
resource = HTTPAuthSessionWrapper(portal, [credentialFactory])
