#-*-coding:utf-8-*-

import plugins
import NormalLink

class Router(object):
	"""docstring for Router"""
	def __init__(self):
		self.routerId = 0			# Router's ID
		self.interfaceIps = []		# Router's interfaces IPs
		self.links = []				# Router's links
		self.areas = []				# Areas which router belongs to
		self.neighborIds = []		# Router's neighborIDs
		self.mapPrefixIp = {}		# Prefix <-> Ip
		self.mapIterfaceLinkid = {}	# InterfaceNo <-> LinkID
		
	def getRouterId(self):
		return self.routerId

	def getInterfaceIps(self):
		return self.interfaceIps

	def getLinks(self):
		return self.links

	def getAreas(self):
		return self.areas

	def getNeighborIds(self):
		return self.neighborIDs

	def setRouterId(self, routerId):
		self.routerId = routerId

	def addInterfaceIp(self, ip):
		self.interfaceIps.append(ip)

	def addLink(self, link):
		self.links.append(link)
		# TODO
		self.mapPrefixIp[link.getPrefix()] = link.getSrcIp()

	def addNeighborId(self, neighborId):
		self.neighborIDs.append(neighborId)

	def addArea(self, area):
		if all([area, area not in self.areas]):
			self.areas.append(area)

	def addInterfaceLinkid(self, interface, linkid):
		if all([interface>=0, linkid>=0]):
			self.mapIterfaceLinkid[interface] = linkid

	def getLinkidByInterface(self, interface):
		return self.mapIterfaceLinkid.get(interface, 0)

	def getPrefixByLinkid(self, linkid):
		# TODO link.getLinkId()
		for link in self.links:
			if link.getLinkId()==linkid:
				return link.getPrefix()
		return 0

	def getIpByPrefix(self, prefix):
		return self.mapPrefixIp.get(prefix, 0)

	def getPrefixByIp(self, ip):
		prefix = [k for k,v in self.mapPrefixIp.iteritems() if v==ip]
		return prefix[0] if prefix else 0