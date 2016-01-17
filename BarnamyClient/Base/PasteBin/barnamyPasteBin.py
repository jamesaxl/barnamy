# -*- coding: utf-8 -*-
import urllib
import urllib2
import re

class BarnamayPastBin(object):

    @classmethod
    def fpaste_scsys(cls, nick, summary, paste):
        
        values = {'channel' : '',
            'nick' : nick,
            'summary' : summary,
            'paste' : paste}

        data = urllib.urlencode(values)
        req = urllib2.Request('http://fpaste.scsys.co.uk/paste', data)
        response = urllib2.urlopen(req)
        page = response.read()
        res = re.search("url=(http://fpaste.scsys.co.uk/[a-zA-Z0-9]+)", page)
        return res.group(1)

    @classmethod
    def bpaste(cls, paste):
        values = {'lexer' : 'text',
                  'expiry' : '1day',
                  'code' : paste}
        data = urllib.urlencode(values)
        req = urllib2.Request('https://bpaste.net/', data)
        response = urllib2.urlopen(req)
        page = response.read()
        res = re.search("/raw/([a-zA-Z0-9]+)", page)
        return 'https://bpaste.net/show/%s' %res.group(1)