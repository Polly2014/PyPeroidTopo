# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

class ExternalLsa(object):
	"""docstring for ExternalLsa"""
	def __init__(self):
		self.metric = 0
		self.advRouter = 0
		self.linkStateId = 0
		self.networkMask = 0
		self.externalType = 0
		self.forwardingAddress = 0

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