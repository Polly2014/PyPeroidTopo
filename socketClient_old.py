# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0


import socket
import sys

HOST = ""
PORT = 9999


if __name__=="__main__":

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Socket Server Created"

	try:
		s.connect((HOST, PORT))
	except socket.error, msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print "Scoket Client Connect Success"

	s.listen(10)
	print "Socket now Listening..."

	while True:
		connection, address = s.accept()
		print "Connected with" + address[0] + ":" + str(address[1])

		data = connection.recv(1024)
		print "Recieved data:{}".format(data)
		reply = "OK..." + data
		if not data:
			connection.sendall("Empty!")
			break

	connection.close()
	s.close()