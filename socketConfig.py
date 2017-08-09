# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import json
import os

SCOKET_CONFIG = {
	#"fileName": "/var/www/html/rtxpert-new-bak/config.json",
	"fileName": "config.json",
	"host": "localhost",
	"port": 9999
}

DB_CONFIG = {
	"engine": "mysql+pymysql",
	"address": "127.0.0.1",
	"username": "root",
	"password": "qazwsx",
	"database": "rtxpert",
	"port": "3306"
}


class socketConfig(object):
	"""docstring for socketConfig"""
	def __init__(self):
		self.config = ""

	def getWebConfig(self):
		if os.path.exists(SCOKET_CONFIG["fileName"]):
			with open(SCOKET_CONFIG["fileName"], "r+") as f:
				self.config = json.loads(f.read())
			print "Web Config File Read Success!"
		else:
			print "Can't find the socket configFile!"		

	def getHostPort(self):
		return SCOKET_CONFIG["host"], SCOKET_CONFIG["port"]

	def judgeHQ(self):
		return self.config["localSet"]["isHQ"]

	def getDBConfig(self):
		DBSet = self.config["localSet"]["localDBSet"]
		#DB_CONFIG["address"] = DBSet["ip"]
		DB_CONFIG["port"] = DBSet["port"]
		DB_CONFIG["database"] = DBSet["dbname"]
		DB_CONFIG["username"] = DBSet["username"]
		DB_CONFIG["password"] = DBSet["password"]
		return DB_CONFIG

	def getProtocol(self):
		return self.config["localSet"]["protocol"]


