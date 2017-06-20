# -*- coding:utf-8 -*-
# S-Scan
# author Nan3r
# 只有TCP方式

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import string,optparse,time
import socket
import threading

#get / ip range
def ip_range(url):
	pos = url.find('/')
	last = int(url[pos+1:])
	ip_list = url[:pos].split('.')
	ip_key = last / 8
	res_list = []
	if ip_key == 1:
		for x in range(1,256):
			for y in range(1,256):
				for z in xrange(1,256):
					res_list.append(ip_list[1] + '.'+str(x) +'.'+str(y) +'.'+str(z))
	if ip_key == 2:
		for x in range(1,256):
			for y in range(1,256):
					res_list.append('.'.join([ip_list[i] for i in range(0, 2)])+ '.'+str(x) +'.'+str(y))
	if ip_key == 3:
		for x in range(1,256):
			res_list.append('.'.join([ip_list[i] for i in range(0, 3)])+ '.'+str(x))
	return res_list


#return url_list
def get_url_list(url):
	url_list = []

	#192.168.1.1-55
	if url.find('-') != -1:
		_url = url.split('-')
		h_url = _url[0].split('.')
		for ip in range(int(h_url[3]), int(_url[1])+1):
			url_list.append('.'.join([h_url[i] for i in range(0, 3)]) + '.'+str(ip) )
		return url_list
	#192.168.22.223/24
	elif url.find('/') != -1:
		return ip_range(url)
	else:
		return url

#return port_list
def get_ports_list(ports):
	ports_list = []

	if ports.find(',') != -1:
		ports_list = ports.split(',')
		return ports_list
	elif ports.find('-') != -1:
		tmp_ports = ports.split('-')
		for port in range(int(tmp_ports[0]), int(tmp_ports[1])+1):
			ports_list.append(port)
		return ports_list
	else:
		return ports

#save result
def save_result(reslut, filename):
	with open(filename, 'w') as f:
		for x in reslut:
			f.writelines(x+"\n")

#url:port scan
#return boolean
def is_open(url, port, timeout):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(timeout)
		s.connect((url, port))
		s.close()
		return True
	except:
		return False

#print result
def print_result(url, port, timeout):
	if is_open(url, int(port), timeout):
		s = "{0}:{1}------------------open".format(url, port)
		print s
		global reslut_list
		reslut_list.append(s)

#threading
# class mythread(threading.Thread):
# 	def __init__(self, url, port, timeout):
# 		threading.Thread.__init__(self)
# 		self.url = url
# 		self.port = port
# 		self.timeout = timeout
# 	def run(self):
# 		threadLock.acquire()
# 		print_result(self.url, self.port, self.timeout)
# 		threadLock.release()
		
#many threads print result
def thread_print_result(urls, ports, timeout, thread_num):
	threads = []
	if isinstance(urls, str):
		if isinstance(ports, str):
			print_result(url, ports, timeout)
		else:
			for port in ports:
				t_my = threading.Thread(target=print_result, args=(urls, port, timeout))
				threads.append(t_my)
				time.sleep(0.001)
	else:
		for url in urls:
			if isinstance(ports, str):
				t_my = threading.Thread(target=print_result, args=(url, ports, timeout))
				threads.append(t_my)
				time.sleep(0.001)
			else:
				for port in ports:
					t_my = threading.Thread(target=print_result, args=(url, port, timeout))
					threads.append(t_my)
					time.sleep(0.001)
	for x in threads:
		x.start()
		while True:
			if len(threading.enumerate()) < thread_num:
				break
	for t in threads:
		t.join()	
		

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-u', '--url', dest='url', help="scan url 192.168.1.1-55 or 192.168.1.1/24")
	parser.add_option('-p', '--port', dest='port', help="scan port 80,8080 or 1-65535")
	parser.add_option('-o', '--out', dest='file', help="save file", default=False)
	parser.add_option('--threads', dest='thread_num', help="default 100", default=100)
	parser.add_option('--timeout', dest='timeout', help="timeout=3", default=3)

	opts, args = parser.parse_args()
	if len(sys.argv) == 1 or len(args) > 0:
		parser.print_help()
		exit()
	if opts.url: urls = get_url_list(opts.url)
	else: 
		print "need a url"
		exit()
	if opts.port: ports = get_ports_list(opts.port)
	else: 
		print "need a port"
		exit()

	#set timeout
	timeout = opts.timeout
	#set filename
	filename = opts.file
	#save result
	reslut_list = []
	#threads
	thread_num = opts.thread_num

	print "Scan Start!   "+str(time.ctime())
	thread_print_result(urls, ports, timeout, thread_num)
	print "Scan Done!    "+str(time.ctime())

	if filename:
		save_result(reslut_list, filename)
		print "the result save in {}".format(filename)
