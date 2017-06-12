# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from enum import Enum
try:
    import cPickle as pickle
except:
    import pickle
from common.AsTopo import AsTopo
from common import plugins


routeType = ("INTERNAL", "INBOUND", "OUTBOUND", "TRANSIT")

class routerAnalyser():
	"""docstring for routerAnalyser"""
	def __init__(self):
		self.topoFilePath = "../topoFile/"
		self.isCorrect = True
		self.hzTopo = {}		# {AsNumber:AsTopo, ...}
		self.result = {}
		pass

	def getHzTopoFromFile(self, topoFilePathName):
		with open(topoFilePathName, 'rb') as f:
			topoFile = pickle.load(f)
		for t in topoFile:
			asTopo = AsTopo()
			asTopo.setAsInfo(t)
			self.hzTopo[asTopo.getAsNumber()] = asTopo
		return True if self.hzTopo else False

	def getOverallRoute(self, topoFileName, srcIp, dstIp, srcMask, dstMask, srcAs, dstAs):
		if all([topoFileName, srcIp, dstIp, srcMask<=0, dstMask<=0]):
			print "Params invalid!"
			return
		topoFilePathName = self.topoFilePath+topoFileName
		ok = self.getHzTopoFromFile(topoFilePathName)
		if not ok:
			return


		srcIp, dstIp = map(plugins.getIdByIp, [srcIp, dstIp])
		# TODO srcAs,dstAs

		curAs = srcAs
		if curAs==dstAs:
			self.getAsRoute(routeType[0], srcIp, srcMask, dstIp, dstMask, 0)

		while curAs!=dstAs:
			if curAs==srcAs:
				getAsRoute(routeType[1], srcIp, srcMask, dstIp, dstMask, 0)
				pass
			elif curAs==dstAs:
				getAsRoute(routeType[2], srcIp, srcMask, dstIp, dstMask, 1)
				pass
			else:
				getAsRoute(routeType[2], srcIp, srcMask, dstIp, dstMask, 1)
				pass


		# print self.ospfTopo
		# return

	def getAsRoute(self, routeType, srcIp, srcMask, dstIp, dstMask, nextHopRouterId):
		asTopo = self.hzTopo.get(0)
		tmpAs = 0
		dstId = 0

		srcId = plugins.getIdByIp(srcIp, srcMask) if nextHopRouterId==0 else nextHopRouterId
		
		if routeType=="INTERNAL" or routeType=="INBOUND":
			dstId = plugins.getIdByIp(dstIp, dstMask)
		else:
			tmp = asTopo.getAsbrIdByPrefix(dstId, dstMask)
			if tmp:
				dstId, nextHopRouterId, tmpAs = tmp
			else:
				print "BGP item for {} can't be found!".format(plugins.getIpById(dstIp))
				return

		if srcId==dstId:
			path = []
			path.append(plugins.getIpById(srcId))
			self.result[curAs] = path





r = routerAnalyser()
r.getOverallRoute("ospf-201705091617.pkl","192.168.100.2","192.168.100.1",123,456,1,2)
