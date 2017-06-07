# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import plugins

class NormalLink(object):
	"""
		docstring for Link
		Router --[link]--> NeighborRouter
	"""
	def __init__(self):
		self.linkId = 0 # Link's ID
		self.metric = 0 # Link's Metric
		self.area = ''	# Area which Link belongs to
		self.srcId = 0	# Link's Src Route ID
		self.mask = 0	# Link's Src Route Mask
		self.dstId = 0	# Link's Dst Route ID
		self.srcIp = 0	# Link's Src Route Interface IP

	def setLinkInfo(self, linkId, metric, area, srcId, dstId, srcIp, mask):
		self.linkId, self.metric, self.area = linkId, metric, area
		self.srcId, self.dstId, self.srcIp = srcId, dstId, srcIp
		self.mask = mask

	def getLinkId(self):
		return self.linkId

	def getMetric(self):
		return self.metric

	def getArea(self):
		return self.area

	def getMask(self):
		return self.mask

	def getSrcId(self):
		return self.srcId

	def getDstId(self):
		return self.dstId

	def getSrcIp(self):
		return self.srcIp

	def getPrefix(self):
		srcIp = plugins.getIpById(self.srcIp)
		mask = plugins.getIpById(self.mask)
		return plugins.getPrefixByIpMask(srcIp, mask)
	
	def setLinkId(self, linkId):
		self.linkId = linkId

	def setMetric(self, metric):
		self.metric = metric

	def setArea(self, area):
		self.area = area

	def setMask(self, mask):
		self.mask = mask

	def setSrcId(self, srcId):
		self.srcId = srcId

	def setDstId(self, dstId):
		self.dstId = dstId

	def setSrcIp(self, srcIp):
		self.srcIp = srcIp