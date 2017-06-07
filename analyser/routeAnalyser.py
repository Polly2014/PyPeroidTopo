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

flowType = ("INTERNAL", "INBOUND", "OUTBOUND", "TRANSIT")

class routerAnalyser():
	"""docstring for routerAnalyser"""
	def __init__(self):
		self.result = {}
		self.topoFilePath = "../topoFile/"
		self.ospfTopo = ""
		self.mapAsTopo = []		# asNum <-> Topo
		pass

	def getOverallRoute(self, topoFileName, srcIp, dstIp, srcMask, dstMask, srcAs, dstAs):
		if all([topoFileName, srcIp, dstIp, srcMask<=0, dstMask<=0]):
			print "Params invalid!"
			return
			
		with open(self.topoFilePath+topoFileName, "rb") as f:
			self.ospfTopo = pickle.load(f)


		if srcAs==dstAs:
			self.getAsRoute(flowType[0], srcIp, srcMask, dstIp, dstMask, 0)



		print self.ospfTopo
		return

	def getAsRoute(self, flowType, srcIp, srcMask, dstIp, dstMask, nextHopRid):
		
		pass

r = routerAnalyser()
r.getOverallRoute("ospf-201705091617.pkl","src","dst",123,456,1,2)
