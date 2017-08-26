#coding:utf-8
#Author: Nan3r
#192.168.1.1/24 255.255.255.0
#192.168.1.1/20 255.255.240.0
#display ip format

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ip = sys.argv[1] or die('Usage:python %s 192.168.1.1/24' % sys.argv[0])
ip4 = int(ip[ip.find('/')+1:])
ipa = ip[:ip.find('/')].split('.')

ipb = []
for i in ipa:
	ipb.append(bin(int(i)))

for x in ipa:
	print "%s 		" % x,
print '\n'

for y in ipb:
	print "{:0>8} 	".format(y[2:]),
print '\n'

ipbstr = ''.join(ipb).replace('0b','')
ip4a = ip4 / 8
ip4b = ip4 % 8

mask = int("{:0<8}".format(ip4b*'1'),2)
if ip4a == 0:
	maskstr = '%s 		0 		0		0' % mask
elif ip4a == 1:
	maskstr = '255		%s 		0		0' % mask
elif ip4a == 2:
	maskstr = '255 		255		%s		0' % mask
elif ip4a == 3:
	maskstr = '255 		255		255		%s' % mask

print maskstr