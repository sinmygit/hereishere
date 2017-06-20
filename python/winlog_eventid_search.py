# -*- coding:utf8 -*-
# ----------------------------
#      Author: Nan3r
#      Date: 2016.7.7
#      Event: eventid search
# ----------------------------

import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
	eventid = sys.argv[1]
	url = 'http://www.eventid.net/display.asp?eventid='+str(eventid)+'&source='

	#提取内容
	html = requests.get(url).text
	soup = BeautifulSoup(html, "lxml")
	result = soup.find_all('table', id='box-table-doc')[0]

	#生成html
	with open(str(eventid)+'.html','w') as f:
		f.write(str(result))
