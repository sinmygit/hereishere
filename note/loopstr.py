#coding:utf-8
#author:Nan3r

import base64
s = 'NTU2NJC3ODHHYWJIZ3P4ZWY='
def dfs(d, t):
	global s
	if d == len(s):
		tmp = base64.b64decode(t)
		#print tmp
		flag = True
		for i in tmp:
			if ord(i) not in (30, 128):
				flag = False
				break
		if flag:
			print tmp
	else:
		dfs(d + 1, t + s[d])
		if 'A' <= s[d] <= 'Z':
			dfs(d + 1, t + chr(ord(s[d]) - ord('A') + ord('a')))
dfs(0, '')