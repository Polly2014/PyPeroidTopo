# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from Bgp import Bgp
from Router import Router
from AsbrLink import AsbrLink
from NormalLink import NormalLink
from ExternalLsa import ExternalLsa
import networkx as nx
import plugins

class AsTopo():
	"""docstring for OspfTopo"""
	def __init__(self):
		self.periodId = 0				# Topo's Peroid ID *
		self.asNumber = 0 				# Topo's AS number *

		self.normalLinks = []			# Topo's normal links
		self.linkIds = []				# Links of Topo *
		self.asbrIds = []				# Topo's ASBRs *
		self.asbrLinks = []				# Links of Topo's ASBRs *
		self.allRouterIds = []			# Topo's Routers

		
		self.mapInterfaceipRouterid = {}# InterfaceIP <-> RouterID [OneRouter] *
		self.mapRouteridRouter = {}		# RouterID <-> Router [OneRouter] *
		self.mapRouteridAsbr = {}		# RouterID <-> Asbr [Asbr]
		self.mapPrefixRouterid = {}		# Prefix <-> RouterID [Stub] *
		self.mapPrefixBgp = {}			# Prefix <-> Bgp [BGP] *
		self.mapPrefixExternallas = {}	# Prefix <-> ExternalLsa [Lsa] *
		self.mapAsbripLinkid = {}		# InterfaceIP <-> LinkID [Asbr] 
		self.mapNexthopAsbrlink = {}	# NextHop <-> AsbrLink *
		
	def __str__(self):
		return "AS:{}\nLinkIds:{}\nRouterIds:{}".format(self.asNumber, self.linkIds, self.routerIds)

	def getPeroidId(self):
		return self.periodId

	def getAsNumber(self):
		return int(self.asNumber)

	def getAsbrIds(self):
		return self.asbrIds

	def getLinkIds(self):
		return self.linkIds

	def getRouterIdByInterfaceIp(self, interfaceIp):
		return self.mapInterfaceipRouterid.get(interfaceIp)

	def getRouterByRouterId(self, routerId):
		return self.mapRouteridRouter.get(routerId)

	def getRouterIdByPrefix(self, prefix):
		return self.mapPrefixRouterid.get(prefix)

	def getBgpByPrefix(self, prefix):
		return self.mapPrefixBgp.get(prefix)

	def getExternalLsaByPrefix(self, prefix):
		return self.mapPrefixExternallas.get(prefix)

	def getAsbrLinkByNextHop(self, nextHop):
		return self.mapNexthopAsbrlink.get(nextHop)

	# BGP
	def getAsbrIdByIpMask(self, ip, mask):
		prefixLength = plugins.getPrefixlenByIpMask(ip, mask)
		while prefixLength>0:
			prefix = plugins.getPrefixByIpMask(ip, prefixLength)
			bgp = self.getBgpByPrefix(prefix)
			if all([bgp, bgp.getPrefixLength()==prefixLength]):
				nextHop = bgp.getNextHop()
				asbrLink = self.getAsbrLinkByNextHop(nextHop)
				if all([asbrLink, bgp.getAsPath()]):
					return [asbrLink.srcId, asbrLink.linkId, \
						bgp.getAsPath(), asbrLink.dstId]
			prefixLength -= 1
		else:
			return

	# InterfaceIp + Stub
	def getAsbrIdByInterfaceIp(self, interfaceIp):
		if interfaceIp<=0:
			return
		asbrId = self.mapInterfaceipRouterid.get(interfaceIp)
		if asbrId:
			return asbrId
		prefix = plugins.getPrefixByIpMask(ip, 32)
		if prefix:
			return self.getRouterIdByPrefix(prefix)

	# ExternalLsa
	def getRouterIdByIpMask(self, ip, mask):
		prefixLength = plugins.getPrefixlenByIpMask(ip, mask)
		while prefixLength>0:
			prefix = plugins.getPrefixByIpMask(ip, prefixLength)
			routerId = self.getRouterIdByPrefix(prefix)
			if routerId:
				return routerId
			externalLsa = self.mapPrefixExternallas.get(prefix)
			if externalLsa and plugins.getIdByIp(externalLsa.networkMask)==plugins.getIdByIp(mask):
				advRouter = externalLsa.getAdvRouter()
				routerId = plugins.getIdByIp(advRouter)
				return routerId
			prefixLength -= 1
		else:
			return

	def getRouterIdFromStub(self, ip, mask):
		prefix = plugins.getPrefixByIpMask(ip, mask)
		routerId = self.mapPrefixRouterid.get(prefix)
		return routerId if routerId else 0

	def getRouterIdFromExternalLsa(self, ip, mask):
		prefix = plugins.getPrefixByIpMask(ip, mask)
		lsa = self.mapPrefixExternallas.get(prefix)
		return lsa.getAdvRouter() if lsa else 0


		'''
		prefix = plugins.getPrefixByIpMask(ip, mask)

		nextHop = 0
		changeCount = 0
		while changeCount<24:
			prefix = plugins.getPrefixByIpMask(ip, mask)
			asbrId = self.mapPrefixBgp.get(prefix)			
			if asbrId:
				bgp = Bgp()
				nextHop = bgp.getNextHop()
				link = getAsbrLinkByNextHop(nextHop)
				if link:
					return [link.srcId, link.dstId, link.dstAs]
			changeCount += 1
			mask <<= 1
		return
		'''

	def getAsbrLinkByNextHop(nextHop):
		for link in self.asbrLinks:
			p1 = plugins.getPrefixByIpMask(link.srcIp, link.mask)
			p2 = plugins.getPrefixByIpMask(nextHop, link.mask)
			if p1==p2:
				return link
		return 

	def getLinkIdByInterfaceIp(self, interfaceIp):
		return self.mapAsbripLinkid.get(interfaceIp)

	def setAsNumber(self, asNumber):
		self.asNumber = asNumber

	def addLinkId(self, linkId):
		self.linkIds.append(linkId)

	def addRouterId(self, routerId):
		if routerId not in self.allRouterIds:
			self.allRouterIds.append(routerId)


	def addMapInterfaceipRouterid(self, interfaceIp, routerId):
		self.mapInterfaceipRouterid[interfaceIp] = routerId

	def addMapRouteridAsbr(routerId, asbr):
		if routerId and asbr:
			self.mapRouteridAsbr[routerId] = asbr

	def addMapRouteridRouter(self, routerId, router):
		self.mapRouteridRouter[routerId] = router

	def addMapPrefixRouterid(self, prefix, routerId):
		if prefix and routerId:
			self.mapPrefixRouterid[prefix] = routerId

	def addAsbrLink(self, asbrLink):
		self.asbrLinks.append(asbrLink)

	def addAsbrId(self, asbrId):
		self.asbrIds.append(asbrId)

	def addMapPrefixBgp(self, prefix, bgp):
		self.mapPrefixBgp[prefix] = bgp

	def setMapPrefixBgp(self, prefix, bgp):
		self.mapPrefixBgp[prefix] = bgp

	def addMapPrefixExternallas(self, prefix, lsa):
		self.mapPrefixExternallas[prefix] = lsa

	def addMapAsbripLinkid(self, interfaceIp, linkId):
		self.mapAsbripLinkid[interfaceIp] = linkId

	def setTopoNodeInfo(self, nodeInfo):
		for node in nodeInfo:
			router = Router()
			routerId = plugins.getIdByIp(node.get("routerId"))
			router.setRouterId(routerId)
			neighbors = node.get("neighbors")
			for neighbor in neighbors:
				srcId = routerId
				linkId = neighbor.get("id")
				area = neighbor.get("area")
				srcIp = plugins.getIdByIp(neighbor.get("interfaceIP"))
				mask = plugins.getIdByIp(neighbor.get("mask"))
				dstId = plugins.getIdByIp(neighbor.get("nRouterId"))
				metric = neighbor.get("metric")
				if all([linkId, srcId, dstId, srcIp, mask]):
					link = NormalLink()
					link.setLinkInfo(linkId, metric, area, srcId, dstId, srcIp, mask)
					router.addArea(area)
					router.addLink(link)
					self.normalLinks.append(link)
					self.addLinkId(linkId)
					self.addMapInterfaceipRouterid(srcIp, srcId)
			self.addRouterId(routerId)
			self.addMapRouteridRouter(routerId, router)


	def setTopoStubInfo(self, stubInfo):
		for stub in stubInfo:
			routerId = plugins.getIdByIp(stub.get("routerId"))
			prefix = stub.get("prefix")
			mask = plugins.getIdByIp(stub.get("mask"))
			if all([routerId, prefix, mask]):
				self.addMapPrefixRouterid(prefix, routerId)

	def setTopoAsbrInfo(self, asbrInfo):
		for asbr in asbrInfo:
			linkId = asbr.get("linkId")
			metric = asbr.get("metric")
			mask = plugins.getIdByIp(asbr.get("mask"))
			srcId = plugins.getIdByIp(asbr.get("routerId"))
			dstId = plugins.getIdByIp(asbr.get("nRouterId"))
			srcIp = plugins.getIdByIp(asbr.get("interfaceIP"))
			dstAs = asbr.get("nAsNumber")
			if all([linkId, srcId, srcIp, mask, dstId, dstAs]):
				asbrLink = AsbrLink()
				asbrLink.setLinkInfo(linkId, metric, mask, \
					srcId, dstId, srcIp, dstAs)
				self.addMapInterfaceipRouterid(srcIp, srcId)
				self.addAsbrLink(asbrLink)
				#self.addAsbrId(srcId)

	def setTopoInfo(self, topoInfo):
		# TODO nodes, stubs, asbrs
		nodeInfo = topoInfo.get("nodes")
		self.setTopoNodeInfo(nodeInfo)
		stubInfo = topoInfo.get("stubs")
		self.setTopoStubInfo(stubInfo)
		asbrInfo = topoInfo.get("InterLink")
		self.setTopoAsbrInfo(asbrInfo)

	def setOuterBgpInfo(self, bgpInfo):
		for bgp in bgpInfo:
			nextHop = plugins.getIdByIp(bgp.get("nexthop"))
			if nextHop==0:
				continue
			prefix = plugins.getIdByIp(bgp.get("prefix"))
			length = bgp.get("length")
			weight = bgp.get("weight")
			origin = bgp.get("origin")
			localPreference = bgp.get("localPreference")
			metric = bgp.get("med")
			asPath = bgp.get("aspath")
			asSize = len(asPath)
			if all([nextHop, prefix, length>=0, weight>=0, origin>=0, \
				localPreference>=0, metric>=0, asSize>=0]):
				b = Bgp()
				b.setBgpInfo(origin, weight, length, metric, prefix, \
					nextHop, localPreference, asPath)
				bTmp = self.mapPrefixBgp.get(prefix)
				if bTmp:
					self.setMapPrefixBgp(prefix, self.bgpRouteSelect(b, bTmp))
				else:
					self.addMapPrefixBgp(prefix, b)

		# for k,v in self.mapPrefixBgp.items():
		# 	print "***[{}] {}".format(self.asNumber, v)
		# print map(plugins.getIpById,self.mapPrefixBgp.keys())


	def setOuterExternallasInfo(self, lsaInfo):
		for lsa in lsaInfo:
			metric = lsa.get("metric")
			networkMask = plugins.getIdByIp(lsa.get("networkMask"))
			advRouter = plugins.getIdByIp(lsa.get("advRouter"))
			linkStateId = plugins.getIdByIp(lsa.get("linkStateId"))
			externalType = lsa.get("externalType")
			forwardingAddress = plugins.getIdByIp(lsa.get("forwardingAddress"))
			if all([networkMask, advRouter, linkStateId, externalType]):
				l = ExternalLsa()
				l.setLsaInfo(metric, advRouter, linkStateId, networkMask, externalType, forwardingAddress)
				self.addMapPrefixExternallas(linkStateId, l)

	def setOuterInfo(self, outerInfo):
		# TODO bgp, externallsa
		bgpInfo = outerInfo.get("BGP")
		self.setOuterBgpInfo(bgpInfo)
		lsaInfo = outerInfo.get("ExternalLsa")
		self.setOuterExternallasInfo(lsaInfo)

	def setAsInfo(self, asInfo):
		asNumber = asInfo.get("asNumber")
		self.setAsNumber(asNumber)
		topoInfo = asInfo.get("Topo")
		self.setTopoInfo(topoInfo)
		outerInfo = asInfo.get("OuterInfo")
		self.setOuterInfo(outerInfo)


	'''
	def setMapAsbrLid(self, ip, linkId):
		if any([ip, linkId]):
			self.mapAsbrLid[ip] = linkId
	
	def setLinkIds(self, id):
		if id:
			self.linkIds.append(id)
	'''


	
	def bgpRouteSelect(self, bgp1, bgp2):
		# 1. Compare The Weight
		w1, w2 = bgp1.getWeight(), bgp2.getWeight()
		if w1!=w2:
			return bgp1 if w1>w2 else bgp2
		# 2. Compare The LocalPreference
		l1, l2 = bgp1.getLocalPreference(), bgp2.getLocalPreference()
		if l1!=l2:
			return bgp1 if l1>l2 else bgp2
		# 3. Compare The As Path Size
		s1, s2 = len(bgp1.getAsPath()), len(bgp2.getAsPath())
		if s1!=s2:
			return bgp1 if s1<s2 else bgp2
		# 4. Compare The Origin
		o1, o2 = bgp1.getOrigin(), bgp2.getOrigin()
		if o1!=o2:
			return bgp1 if o1<o2 else bgp2
		# 5. Compare The Med
		m1, m2 = bgp1.getMetric(), bgp2.getMetric()
		if m1!=m2:
			return bgp1 if m1<m2 else bgp2
		return bgp1
	'''
	def getShortestPaths(self, srcId, dstId):
		g = nx.DiGraph(asNumber = self.asNumber)
		edges = [link.getEdge() for link in self.normalLinks]
		g.add_weighted_edges_from(edges)
		s = plugins.getIpById(srcId)
		t = plugins.getIpById(dstId)
		paths = nx.all_shortest_paths(G=g, source=s, target=t, weight="weight")
		return list(paths)
	'''
	def getShortestPaths(self, srcSeg, dstSeg):
		result = {"code":0, "message":""}
		g = nx.DiGraph(asNumber = self.asNumber)
		edges = [link.getEdge() for link in self.normalLinks]
		g.add_weighted_edges_from(edges)
		s, t = map(self.getRouterIdByNetSegment, [srcSeg, dstSeg])
		print "Source:{}->Target:{}".format(s,t)
		if s==t:
			result["code"] = 1
			result["message"] = [s]
			return result
		try:
			paths = nx.all_shortest_paths(G=g, source=s, target=t, weight="weight")
			result["code"] = 1
			result["message"] = list(paths)
		except Exception, e:
			result["message"] = "Path Found Error: {}-{}".format(Exception, e)
		return result
		#return list(paths) if paths else None

	# Stub or Router's Interface
	def getRouterIdByNetSegment(self, netSegment):
		ns = netSegment.int()
		if netSegment.prefixlen()==32:
			return plugins.getIpById(ns) if ns in self.allRouterIds \
				else plugins.getIpById(self.mapInterfaceipRouterid.get(ns))
		else:
			return plugins.getIpById(self.mapPrefixRouterid.get(ns))
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

	# ExternalLsa
	def getAsbrSegByDstSegment(self, netSegment):
		prefixLength = netSegment.prefixlen()
		ns = netSegment.int()
		while prefixLength>0:
			prefix = plugins.getPrefixByIpMask(ns, prefixLength)
			externalLsa = self.mapPrefixExternallas.get(prefix)
			if externalLsa and externalLsa.getPrefixLength()==prefixLength:
				asbrId = externalLsa.getAdvRouter()
				return plugins.getNetSegmentByIpMask(asbrId)
			prefixLength -= 1
		else:
			return "Oh, No"

	# AsbrLink
	def getNextHopsByAsbrSegment(self, asbrSegment):
		nextHopSegs = []
		for asbrLink in self.asbrLinks:
			netSegment = plugins.getNetSegmentByIpMask(asbrLink.srcId)
			if netSegment==asbrSegment:
				nextHopSeg = plugins.getNetSegmentByIpMask(asbrLink.dstId)
				nextHopSegs.append(nextHopSeg)
		return nextHopSegs

	# BGP
	def getNextHopByNetSegment(self, netSegment, nextHops):
		print "dstSegment:{}".format(netSegment.strNormal())
		prefixLength = netSegment.prefixlen()
		ns = netSegment.int()
		while  prefixLength>0:
			prefix = plugins.getPrefixByIpMask(ns, prefixLength)
			bgp = self.mapPrefixBgp.get(prefix)
			print "###prefix:{}, BGP:{}".format(prefixLength, bgp)
			if bgp and bgp.prefixLength==prefixLength:
				nextHop = plugins.getNetSegmentByIpMask(bgp.nextHop)
				if nextHop in nextHops:
					return nextHop
			prefixLength -= 1
		else:
			return netSegment
			#return "Oh! No! Couldn't find the nextHop >_<"

	# BGP & Asbr
	'''
	def getNextHopBySegments(self, asbrSegment, dstSegment):
		prefixLength = netSegment.prefixlen()
		ns = netSegment.int()
		while  prefixLength>0:
			prefix = plugins.getPrefixByIpMask(ns, prefixLength)
			bgp = self.mapPrefixBgp.get(prefix)
			if bgp and bgp.prefixLength==prefixLength:
				nextHop = bgp.getNextHop()
				print "nextHop-{}".format(plugins.getIpById(nextHop))
				return plugins.getNetSegmentByIpMask(nextHop)
			prefixLength -= 1
		else:
			return "Oh! No!"
	'''

