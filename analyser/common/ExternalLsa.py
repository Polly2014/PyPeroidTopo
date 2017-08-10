# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import plugins

class ExternalLsa(object):
	"""
		example = {
			"metric": 0,
			"advRouter": 19239192,	//"192.168.5.2"
			"linkStateId": 1021030,	//"192.168.13.0"
			"networkMask": 1101010, //"255.255.255.0"
			"externalType": 2,
			"forwardingAddress": 0,	//"0.0.0.0"
		}
	"""
	def __init__(self):
		self.metric = 0
		self.advRouter = 0
		self.linkStateId = 0
		self.networkMask = 0
		self.externalType = 0
		self.forwardingAddress = 0

	def __str__(self):
		advRouter = plugins.getIpById(self.advRouter)
		prefix = plugins.getNetSegmentByIpMask(self.linkStateId, self.networkMask)
		return "Go To{}, From Asbr{}".format(prefix, advRouter)

	def __eq__(self, lsa):
		return all([self.metric==lsa.metric, self.linkStateId==lsa.linkStateId, \
			self.advRouter==lsa.advRouter])

	def __lt__(self, lsa):
		return self.metric<lsa.metric

	def setLsaInfo(self, m, a, l, n, e, f):
		self.metric, self.advRouter, self.linkStateId = m, a, l
		self.networkMask, self.externalType, self.forwardingAddress = n, e, f
		
	def getMetric(self):
		return self.metric

	def getAdvRouter(self):
		return self.advRouter

	def getLinkStateId(self):
		return self.linkStateId

	def getNetwrokMask(self):
		return self.networkMask

	def getExternalType(self):
		return self.externalType

	def getForwardingAddress(self):
		return self.forwardingAddress

	def getPrefixLength(self):
		return plugins.getPrefixlenByMask(self.networkMask)