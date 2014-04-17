import socket
import os
import json

webs = {}
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if os.path.exists('/tmp/spider_tmp'):
	os.remove('/tmp/spider_tmp')

sock.bind('/tmp/spider_tmp')
sock.listen(10)

while True:
	connection, address = sock.accept()
	data = connection.recv(1024*1024)
	# datajson = json.loads(data)
	print "receive from:",data
	# for title in datajson['titles']:
	# 	print title
