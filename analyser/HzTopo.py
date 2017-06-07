#-*-coding:utf-8-*-

from common.AsTopo import AsTopo
try:
    import cPickle as pickle
except:
    import pickle


def prn_obj(obj):
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def getHzTopoFromFile(topoFilePathName):
	hzTopo = []

	with open(topoFilePathName, 'rb') as f:
		topoFile = pickle.load(f)

	for t in topoFile:
		asTopo = AsTopo()
		asTopo.setAsInfo(t)
		hzTopo.append(asTopo)

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
for asTopo in hzTopo:
	print dir(asTopo)
	print "----------------------------------"