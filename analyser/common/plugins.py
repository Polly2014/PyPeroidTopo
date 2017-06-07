#-*-coding:utf-8-*-

from IPy import IP

def getPrefixByIpMask(ip, mask):
	return IP(ip).make_net(mask).int()

def getIdByIp(ip):
	return IP(ip).int()

def getIpById(id):
	return IP(id).strNormal()

