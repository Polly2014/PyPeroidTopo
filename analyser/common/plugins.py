# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from IPy import IP

def getPrefixByIpMask(ip, mask):
	return IP(ip).make_net(mask).int()

def getIdByIp(ip):
	return IP(ip).int()

def getIpById(id):
	return IP(id).strNormal()
