# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import json
import os

CONFIG = {
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
		if os.path.exists(CONFIG["fileName"]):
			with open(CONFIG["fileName"], "r+") as f:
				self.config = json.loads(f.read())
			print "Config File Read Success!"
		else:
			print "Can't find the configFile!"

	def getHostPort(self):
		return CONFIG["host"], CONFIG["port"]

	def judgeHQ(self):
		return self.config["localSet"]["isHQ"]

	def getDBConfig(self):
		return DB_CONFIG


