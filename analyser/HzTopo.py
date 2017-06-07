# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from common.AsTopo import AsTopo
try:
    import cPickle as pickle
except:
    import pickle


def prn_obj(obj):
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def getHzTopoFromFile(topoFilePathName):
	hzTopo = {}

	with open(topoFilePathName, 'rb') as f:
		topoFile = pickle.load(f)

	for t in topoFile:
		asTopo = AsTopo()
		asTopo.setAsInfo(t)
		hzTopo[asTopo.getAsNumber()] = asTopo

	return hzTopo
	


def getTopoInfoFromFile(topoFile):
	pass

def getBgpInfoFromFile(topoFile):
	pass

def getElasInfoFromFile(topoFile):
	pass

def getPrefixByIpMask(ip, mask):
	return IP(ip).make_net(mask).int()

def getIdByIp(ip):
	return IP(ip).int()



hzTopo = getHzTopoFromFile("../topoFile/ospf-201705091617.pkl")
print hzTopo