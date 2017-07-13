# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import plugins

class Bgp(object):
	"""
		BGP class
		# 1.Prefer the path with the highest WEIGHT.
		# 2.Prefer the path with the highest LOCAL_PREF.
		# 3.Prefer the path that was locally originated via a network 
		    or aggregate BGP subcommand 
		    or through redistribution from an IGP.nexthop=0.0.0.0
		# 4.Prefer the path with the shortest AS_PATH.
		# 5.Prefer the path with the lowest origin type.
		# 6.Prefer the path with the lowest multi-exit discriminator(MED).
	"""
	def __init__(self):
		self.origin = 0
		self.weight = 0				# Uses in Cisco
		self.prefixLength = 0		# Count of 1 in mask
		self.med = 0				# range from 0 to 4,294,967,294
		self.prefix = 0				#
		self.nextHop = 0			#
		self.localPreference = 0	#
		self.asPath = []

	def __str__(self):
		prefixLength = self.prefixLength
		prefix, nextHop = map(plugins.getIpById, [self.prefix, self.nextHop])
		return "Go to {}/{}\tNextHop {}".format(prefix, prefixLength, nextHop)

	def __eq__(self, bgp):
		return all([self.prefix==bgp.prefix, self.prefixLength==bgp.prefixLength, \
			self.nextHop==bgp.nextHop])

	def setBgpInfo(self, origin, weight, prefixLength, metric, prefix, \
			nextHop, localPreference, asPath):
		self.origin, self.weight, self.prefixLength = origin, weight, prefixLength
		self.med, self.prefix, self.nextHop = metric, prefix, nextHop
		self.localPreference, self.asPath = localPreference, asPath

	def getOrigin(self):
		return self.origin

	def getWeight(self):
		return self.weight

	def getPrefixLength(self):
		return self.prefixLength

	def getMetric(self):
		return self.med

	def getPrefix(self):
		return self.prefix

	def getNextHop(self):
		return self.nextHop

	def getLocalPreference(self):
		return self.localPreference

	def getAsPath(self):
		return self.asPath

	def setOrigin(self, origin):
		self.origin = origin

	def setWeight(self, weight):
		self.weight = weight

	def setLength(self, prefixLength):
		self.prefixLength = prefixLength

	def setMetric(self, med):
		self.med = med

	def setPrefix(self, prefix):
		self.prefix = prefix

	def setNextHop(self, nextHop):
		self.nextHop = nextHop

	def setLocalPreference(self, localPreference):
		self.localPreference = localPreference

	def setAsPath(self, asPath):
		self.asPath = asPath

	def showDetail(self):
		prefix, nextHop = map(plugins.getIpById, [self.prefix, self.nextHop])
		return "Origin:{}, Weight:{}, PrefixLength:{}, Metric:{}, Prefix:{}, \
			NextHop:{}, LocalPreference:{}, AsPath:{}".format(self.origin, \
			self.weight, self.prefixLength, self.med, prefix, nextHop, \
			self.localPreference, self.asPath)

	def getPrefixLength(self):
		return plugins.getPrefixlenByMask(self.prefix)