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
import plugins

class AsTopo():
	"""docstring for OspfTopo"""
	def __init__(self):
		self.periodId = 0				# Topo's Peroid ID *
		self.asNumber = 0 				# Topo's AS number *
		self.asbrIds = []				# Topo's ASBRs
		self.linkIds = []				# Links of Topo *
		self.asbrLinks = []				# Links of Topo's ASBRs *
		self.routerIds = []				# Topo's Routers

		self.mapIpRouterid = {}			# Ip <-> RouterID *
		self.mapRouteridRouter = {}		# RouterID <-> Router *
		self.mapPrefixRouterid = {}		# Prefix <-> RouterID *
		self.mapPrefixBgp = {}			# Prefix <-> Bgp *
		self.mapPrefixExternallas = {}	# Prefix <-> ExternalLsa *
		self.mapAsbrLid = {}			# Asbr <-> LinkID
		self.mapAsbrRid = {}			# Asbr <-> RouterID
		
	def __str__(self):
		return "AS:{}\nLinkIds:{}\nRouterIds:{}".format(self.asNumber, self.linkIds, self.routerIds)

	def getPeroidId(self):
		return self.periodId

	def getAsNumber(self):
		return self.asNumber

	def getAsbrIds(self):
		return self.asbrIds

	def getRouterByRid(rid):
		return self.mapRouterRid.get(rid)

	def getAsbrByPre(ip, mask):
		# TODO
		pass

	def setAsNumber(self, asNumber):
		self.asNumber = asNumber

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
				if all([linkId, area, srcId, dstId, srcIp, mask]):
					link = NormalLink()
					link.setLinkInfo(linkId, metric, area, srcId, dstId, srcIp, mask)
					router.addArea(area)
					router.addLink(link)
					self.addLinkId(linkId)
					self.addMapIpRouterid(srcIp, srcId)
			self.addMapRouteridRouter(routerId, router)

	def setTopoStubInfo(self, stubInfo):
		for stub in stubInfo:
			routerId = stub.get("routerId")
			prefix = stub.get("prefix")
			mask = stub.get("mask")
			if all([routerId, prefix, mask]):
				self.addMapPrefixRouterid(prefix, routerId)

	def setTopoAsbrInfo(self, asbrInfo):
		for asbr in asbrInfo:
			linkId = asbr.get("linkId")
			interfaceNo = 0
			metric = asbr.get("metric")
			mask = plugins.getIdByIp(asbr.get("mask"))
			srcId = plugins.getIdByIp(asbr.get("routerId"))
			dstId = plugins.getIdByIp(asbr.get("nRouterId"))
			srcIp = plugins.getIdByIp(asbr.get("interfaceIP"))
			dstAs = asbr.get("nAsNumber")
			if all([linkId, srcId, srcIp, mask, dstId, dstAs]):
				asbrLink = AsbrLink()
				asbrLink.setLinkInfo(linkId, interfaceNo, metric, \
					mask, srcId, dstId, srcIp, dstAs)
				self.addMapIpRouterid(srcIp, srcId)
				self.addAsbrLink(asbrLink)

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
				localPreference>=0, metric>=0, asSize]):
				b = Bgp()
				b.setBgpInfo(origin, weight, length, metric, prefix, \
					nexthop, localPreference, asPath)
				bTmp = self.mapPrefixBgp.get(prefix)
				if bTmp:
					self.setMapPrefixBgp(prefix, self.bgpRouteSelect(b, bTmp))
				else:
					self.addMapPrefixBgp(prefix, b)

	def setOuterExternallasInfo(self, lsaInfo):
		for lsa in lsaInfo:
			metric = lsa.get("metric")
			networkMask = plugins.getIdByIp(lsa.get("networkMask"))
			advRouter = plugins.getIdByIp(lsa.get("advRouter"))
			linkStateId = plugins.getIdByIp(lsa.get("linkStateId"))
			externalType = lsa.get("externalType")
			forwardingAddress = plugins.getIdByIp(lsa.get("forwardingAddress"))
			if all([networkMask, advRouter, linkStateId, externalType, forwardingAddress]):
				l = ExternalLsa()
				l.setLsaInfo(metric, networkMask, advRouter, linkStateId, externalType, forwardingAddress)
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

	def setMapAsbrLid(self, ip, linkId):
		if any([ip, linkId]):
			self.mapAsbrLid[ip] = linkId

	def setLinkIds(self, id):
		if id:
			self.linkIds.append(id)

	def addLinkId(self, linkId):
		self.linkIds.append(linkId)

	def addMapIpRouterid(self, ip, routerId):
		self.mapIpRouterid[ip] = routerId

	def addMapRouteridRouter(self, routerId, router):
		self.mapRouteridRouter[routerId] = router

	def addMapPrefixRouterid(self, prefix, routerId):
		self.mapPrefixRouterid[prefix] = plugins.getIdByIp(routerId)

	def addAsbrLink(self, asbrLink):
		self.asbrLinks.append(asbrLink)

	def addMapPrefixBgp(self, prefix, bgp):
		self.mapPrefixBgp[prefix] = bgp

	def addMapPrefixExternallas(self, prefix, lsa):
		self.mapPrefixExternallas[prefix] = lsa

	def setMapPrefixBgp(self, refix, bgp):
		self.mapPrefixBgp[prefix] = bgp
	
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
		return m1
