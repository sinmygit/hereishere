#coding:utf-8
from bs4 import BeautifulSoup
import requests

'''
搜索列目录中的文件
'''
def getHtml(url):
	headers = {
				'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)'
			}
	return requests.get(url, headers=headers).text


def isfloder(name):
	if name[-1:] == '/':
		return True
	return False

'''
1.'Up To '
2.'Parent Directory'

字符串中包含这两种就返回FALSE
'''
def isSave(name):
	if name.find('Up To') != -1 or name.find('Parent Directory') != -1:
		return False
	return True

'''
获取当前路径的文件夹及文件
<a href='xxx'>xxx</a>
return:
{
	'path':'asdas/fasfas/',
	'floders':[a,b,c],
	'files':[q,w,r,t]
}
'''
def getNowALLFiles(url):
	global resultF
	tmpF = ''
	result = {}
	result['path'] = url
	result['floders'] = []
	result['files'] = []
	html = getHtml(url)
	soup = BeautifulSoup(html, 'lxml')
	if len(soup.find_all('a')):
		for taga in soup.find_all('a'):
			tmpF = taga.get_text().strip()
			if not isSave(tmpF):
				continue
			if isfloder(tmpF):
				result['floders'].append(tmpF)
				getNowALLFiles(url+tmpF)
			else:
				result['files'].append(tmpF)
	resultF.append(result)

'''
main
'''
def main(url, search):
	'''
	获取整个目录结果保存到resultF中
	'''
	getNowALLFiles(url)

	# for i in resultF:
	# 	print i

	searchResult = []
	tmp = ''
	for i in resultF:
		for file in i['files']:
			if file.find(search) != -1:
				tmp = i['path']+file
				searchResult.append(tmp)
	return searchResult


if __name__ == '__main__':
	'''
	http://www.dclunie.com/images/
	'''
	resultF = []
	import sys
	if len(sys.argv) != 3:
		print 'Example: python %s (http://|https://)url search' % sys.argv[0]
		exit()

	url = sys.argv[1]
	'''
	查找字符串中包含某字符的文件
	'''
	search = sys.argv[2]
	allFile = main(url, search)
	print allFile