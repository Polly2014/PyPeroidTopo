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
		self.result = {"code":-1, "message":[]}

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

		# Step 1: (ip, mask) => netSegment
		srcSeg = plugins.getNetSegmentByIpMask(srcIp, srcMask)
		dstSeg = plugins.getNetSegmentByIpMask(dstIp, dstMask)
		print "srcSeg:{}, dstSeg:{}".format(srcSeg, dstSeg)

		# Step 2: netSegment => asNumber
		srcAs, dstAs = map(self.getAsNumberByNetSegment, [srcSeg, dstSeg])
		if all([srcAs>-1, dstAs>-1]):
			print "srcAs:{}, dstAs:{}".format(srcAs, dstAs)
		

		curAs = srcAs
		if curAs==dstAs:
			asPath = self.getAsPath(curAs, "INTERNAL", srcSeg, dstSeg)
			#path = self.getAsRoute(curAs, "INTERNAL", srcIp, srcMask, dstIp, dstMask, 0)
			self.result.append(asPath)
		no = 0
		while curAs!=dstAs:
			print "@@@The {}-times running...".format(no+1)
			if curAs==srcAs:
				print "curAs==srcAS"
				srcSeg = self.getAsPath(curAs, "OUTBOUND", srcSeg, dstSeg)
				curAs = self.getAsNumberByNetSegment(srcSeg)
				print "nextAs: {}".format(curAs)
				#self.getAsRoute(curAs, "OUTBOUND", srcIp, srcMask, dstIp, dstMask, 0)
			elif curAs==dstAs:
				print "curAs==dstAs"
				asPath = self.getAsPath(curAs, "INBOUND", srcSeg, dstSeg)
				#self.getAsRoute(curAs, "INBOUND", srcIp, srcMask, dstIp, dstMask, 1)
				pass
			else:
				self.getAsRoute(curAs, "TRANSIT", srcIp, srcMask, dstIp, dstMask, 1)
				pass
			no += 1
		else:
			print "@@@The {}-times running...".format(no+1)
			print "curAs==dstAS"
			self.getAsPath(curAs, "INBOUND", srcSeg, dstSeg)
			#path = self.getAsRoute(curAs, "INTERNAL", srcIp, srcMask, dstIp, dstMask, 0)
			#print asPath
			#break
		#print "Result:{}".format(self.result)


		# print self.ospfTopo
		# return

	def getAsPath(self, asNum, pathType, srcSeg, dstSeg):
		asTopo = self.hzTopo.get(asNum)
		print map(plugins.getIpById,asTopo.allRouterIds)
		print "Normal Links:"
		for link in  asTopo.normalLinks:
			print link
		print "-----------------"
		print "Asbr Links:"
		for link in asTopo.asbrLinks:
			print link
		print "-----------------"

		if pathType=="INTERNAL" or pathType=="INBOUND":
			paths = asTopo.getShortestPaths(srcSeg, dstSeg)
			print paths
			return {asNum:paths}
		else:	# OUTBOUND OR TRANSIT
			asbrSeg = asTopo.getAsbrIdByNetSegment(dstSeg)
			print "asbrSeg:{}".format(asbrSeg)
			paths = asTopo.getShortestPaths(srcSeg, asbrSeg)
			print paths
			nextHop = asTopo.getNextHopByNetSegment(dstSeg)
			print "nextHop:{}".format(nextHop)
			return nextHop
			# for k,v in asTopo.mapPrefixBgp.items():
			# 	ip = plugins.getIpById(k)
			# 	info = v.showDetail()
			# 	print "GBP\n{}\n{}".format(ip, info)
			# 	print "###############"
			# nextAs = asTopo.
			# nextSrcSeg = asTopo.









	def getAsRoute(self, asNum, routeType, srcIp, srcMask, dstIp, dstMask, nextHopRouterId):
		asTopo = self.hzTopo.get(asNum)
		print [plugins.getIpById(r) for r in asTopo.allRouterIds]
		print "Normal Links:"
		for link in  asTopo.normalLinks:
			print link
		print "_____________________"
		print "Asbr Links:"
		for link in asTopo.asbrLinks:
			print link
		print "_____________________"
		print "InterfaceIp <-> Router:"
		for k,v in asTopo.mapInterfaceipRouterid.items():
			interfaceIp, routerId = map(plugins.getIpById, [k,v])
			print "{} <-> {}".format(interfaceIp, routerId)
		print "_____________________"

		if routeType=="INTERNAL" or routeType=="INBOUND":
			paths = asTopo.getShortestPaths(srcIp, dstIp)
			return {asNum:paths}





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





r = routerAnalyser()
r.getOverallRoute("ospf-201706282037.pkl","192.168.2.1","192.168.14.2",32,32,1,1)
