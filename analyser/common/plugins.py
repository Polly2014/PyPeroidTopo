# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from IPy import IP
import NormalLink, AsbrLink

def getNetSegmentByIpMask(ip, mask):
	ip = IP(ip) if isinstance(ip, long) else ip
	mask = IP(mask) if isinstance(mask, long) else mask
	return IP(ip).make_net(mask)

def getPrefixByIpMask(ip, mask):
	ip = IP(ip) if isinstance(ip, long) else ip
	mask = IP(mask) if isinstance(mask, long) else mask
	return IP(ip).make_net(mask).int()

def getPrefixlenByIpMask(ip, mask):
	if isinstance(mask, int):
		return mask
	ip = IP(ip) if isinstance(ip, long) else ip
	mask = IP(mask) if isinstance(mask, long) else mask
	return IP(ip).make_net(mask).prefixlen()

def getPrefixlenByMask(mask):
	if isinstance(mask, int):
		return mask
	else:
		return IP(mask).strBin().count('1')


def getIdByIp(ip):
	return IP(ip).int()

def getIpById(id):
	return IP(id).strNormal()


