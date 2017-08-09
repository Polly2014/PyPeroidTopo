# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from IPy import IP
import NormalLink, AsbrLink

def getNetSegmentByIpMask(ip, mask=32):
	try:
		ip = IP(ip) if isinstance(ip, long) else ip
		if not isinstance(mask, str):
			mask = IP(mask) if mask>32 else mask
		#mask = IP(mask) if isinstance(mask, long) else mask
		return IP(ip).make_net(mask)
	except Exception, e:
		print "$$$ netSegment Error:{}-{}".format(Exception, e)

def getPrefixByIpMask(ip, mask):
	#print "Before<<IP:{}[{}], Mask:{}[{}]>>".format(ip,type(ip), mask, type(mask))
	try:
		ip = IP(ip) if isinstance(ip, long) else ip
		if not isinstance(mask, str):
			mask = IP(mask) if mask>32 else mask
		#mask = IP(mask) if not isinstance(mask, str) else mask
		#print "After<<IP:{}[{}], Mask:{}[{}]>>".format(ip,type(ip), mask, type(mask))
		return IP(ip).make_net(mask).int()
	except Exception, e:
		print "$$$ getPrefix Error:{}-{}".format(Exception, e)
	

def getPrefixlenByIpMask(ip, mask):
	ip = IP(ip) if isinstance(ip, long) else ip
	if not isinstance(mask, str):
		mask = IP(mask) if mask>32 else mask
	return IP(ip).make_net(mask).prefixlen()

def getPrefixlenByMask(mask):
	if not isinstance(mask, str):
		return IP(mask).strBin().count('1') if mask>32 else mask
	else:
		return IP(mask).strBin().count('1')


def getIdByIp(ip):
	return IP(ip).int()

def getIpById(id):
	return IP(id).strNormal()


