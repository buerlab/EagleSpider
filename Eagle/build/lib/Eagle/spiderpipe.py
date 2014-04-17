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
	data = connection.recv(16*1024)
	webAccept = json.loads(data)
	print "receive from:",webAccept['weburl']
	for title in webAccept['titles']:
		print title
