# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0


import socket
import sys

HOST = ""
PORT = 9999



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket Server Created"

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print "Scoket Server Bind Complete"

s.listen(10)
print "Socket now Listening..."

while True:
	conn, addr = s.accept()
	print "Connected with" + addr[0] + ":" + str(addr[1])

	data = conn.recv(1024)
	reply = "OK..." + data
	if not data:
		break
	conn.sendall(reply)

conn.close()
s.close()