# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import socket
import threading
import SocketServer
import json


def client(host, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	try:
		sock.sendall(message)
		response = sock.recv(1024)
		print "Received: {}".format(response)
	finally:
		sock.close()

if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "localhost", 9999

	s = {
		'pid': '201707282039',
		'srcIp': '192.168.2.2',
		'dstIp': '192.168.14.2',
		'srcMask': 32,
		'dstMask': 32,
		'srcAs': 1,
		'dstAs': 1
	}

	# s = {
	# 	'pid': '201707282039',
	# 	'srcIp': '192.168.1.0',
	# 	'dstIp': '192.168.5.0'
	# }
	client(HOST, PORT, json.dumps(s))
	# for i in range(2):
	#     client(HOST, PORT, "hello world-{}".format(i+1))