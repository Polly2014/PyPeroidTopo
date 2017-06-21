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
import networkx as nx


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

		srcSeg = plugins.getNetSegmentByIpMask(srcIp, srcMask)
		dstSeg = plugins.getNetSegmentByIpMask(dstIp, dstMask)

		# srcRouter = 
		# dstRouter = 

		srcIp, dstIp = map(plugins.getIdByIp, [srcIp, dstIp])
		srcAs, dstAs = map(self.getAsNumberByNetSegment, [srcSeg, dstSeg])
		if all([srcAs>-1, dstAs>-1]):
			print "srcAs:{}, dstAs:{}".format(srcAs, dstAs)
		

		curAs = srcAs
		if curAs==dstAs:
			self.getAsRoute(curAs, "INTERNAL", srcIp, srcMask, dstIp, dstMask, 0)

		while curAs!=dstAs:
			if curAs==srcAs:
				getAsRoute(curAs, "OUTBOUND", srcIp, srcMask, dstIp, dstMask, 0)
				pass
			elif curAs==dstAs:
				getAsRoute(curAs, "INBOUND", srcIp, srcMask, dstIp, dstMask, 1)
				pass
			else:
				getAsRoute(curAs, "TRANSIT", srcIp, srcMask, dstIp, dstMask, 1)
				pass


		# print self.ospfTopo
		# return

	def getAsRoute(self, asNum, routeType, srcIp, srcMask, dstIp, dstMask, nextHopRouterId):
		asTopo = self.hzTopo.get(asNum)
		print [plugins.getIpById(r) for r in asTopo.allRouterIds]

		for link in  asTopo.normalLinks:
			print link
		print "_____________________"
		for link in asTopo.asbrLinks:
			print link
		print "_____________________"
		for k,v in asTopo.mapInterfaceipRouterid.items():
			interfaceIp, routerId = map(plugins.getIpById, [k,v])
			print "{} <-> {}".format(interfaceIp, routerId)
		print "_____________________"
		if routeType=="INTERNAL":
			paths = asTopo.getShortestPaths(srcIp, dstIp)
			for p in paths:
				print p




			# as_graph = nx.DiGraph(asNumber=asNum)
			# edges = [link.getEdge() for link in asTopo.normalLinks]
			# as_graph.add_weighted_edges_from(edges)
			# s = plugins.getIpById(srcIp)
			# t = plugins.getIpById(dstIp)
			# paths = nx.all_shortest_paths(as_graph, source=s, target=t, weight="weight")
			# paths = list(paths)
			# print "{} Paths Founded!".format(len(paths))
			# #print paths
			# for p in paths:
			# 	print p
			#print paths[srcIp][dstIp]
			# pass

		'''
		srcId = plugins.getPrefixByIpMask(srcIp, srcMask) if nextHopRouterId==0 else nextHopRouterId
		
		if routeType=="INTERNAL" or routeType=="INBOUND":
			dstId = asTopo.getRouterIdByIpMask(dstIp, dstMask)
		else:
			asbrId = asTopo.getAsbrIdByIpMask(dstId, dstMask)
			if asbrId:
				srcId, linkId, asPath, dstId = asbrId
			else:
				print "BGP item for {} can't be found!".format(plugins.getIpById(dstIp))
				return

		if srcId==dstId:
			path = []
			path.append(plugins.getIpById(srcId))
			self.result[curAs] = path
		'''

	def getAsNumberByNetSegment(self, netSegment):
		ns = netSegment.int()
		for asNumber,asTopo in self.hzTopo.items():
			if (ns in asTopo.allRouterIds) or asTopo.mapPrefixRouterid.has_key(ns):
				return asNumber
		else:
			return -1
		'''
		if netSegment.prefixlen()==32:
			for asNumber,asTopo in self.hzTopo.items():
				if routerId in asTopo.allRouterIds:
					return asNumber
			else:
				return -1
		else:
			for asNumber,asTopo in self.hzTopo.items():
				if asTopo.mapPrefixRouterid.has_key(routerId):
					return asNumber
			else:
				return -1
		'''

	def getRouterIdByNetSegment(self, netSegment):
		pass




r = routerAnalyser()
r.getOverallRoute("ospf-201706201617.pkl","192.168.2.1","192.168.5.1",24,24,1,1)
