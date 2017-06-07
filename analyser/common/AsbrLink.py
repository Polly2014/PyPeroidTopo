# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import plugins

class AsbrLink(object):
	"""
		Link belongs to Asbr

	"""
	def __init__(self):
		self.linkId = 0 		# Link's ID
		self.interfaceNo = 0	# Interface Index No.
		self.metric = 0 		# Link's Metric
		self.mask = 0			# Link's Src Route Mask
		self.srcId = 0			# Link's Src Route ID
		self.dstId = 0			# Link's Dst Route ID
		self.srcIp = 0			# Link's Src Route Interface IP
		self.dstAs = 0			# Link's Dst AS Number

	def setLinkInfo(self, linkId, interfaceNo, metric, mask, \
			srcId, dstId, srcIp, dstAs):
		self.linkId, self.interfaceNo, self.metric = linkId, interfaceNo, metric
		self.srcId, self.dstId = srcId, dstId
		self.srcIp, self.dstAs = srcIp, dstAs

	def getLinkId(self):
		return self.linkId

	def getInterfaceNo(self):
		return self.interfaceNo

	def getMetric(self):
		return self.metric

	def getMask(self):
		return self.mask

	def getSrcId(self):
		return self.srcId

	def getDstId(self):
		return self.dstId

	def getSrcIp(self):
		return self.srcIp

	def getDstAs(self):
		return self.dstAs

	def getPrefix(self):
		return plugins.getPrefixByIpMask(self.srcIp, self.mask)
	
	def setLinkId(self, linkId):
		self.linkId = linkId

	def setInterfaceNo(self, interfaceNo):
		self.interfaceNo = interfaceNo

	def setMetric(self, metric):
		self.metric = metric

	def setMask(self, mask):
		self.mask = mask

	def setSrcId(self, srcId):
		self.srcId = srcId

	def setDstId(self, dstId):
		self.dstId = dstId

	def setSrcIp(self, srcIp):
		self.srcIp = srcIp

	def setDstAs(self, dstAs):
		self.dstAs = dstAs