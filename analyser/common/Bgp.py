#-*-coding:utf-8-*-

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
		self.length = 0				# Count of 1 in mask
		self.med = 0				# range from 0 to 4,294,967,294
		self.prefix = 0				#
		self.nextHop = 0			#
		self.localPreference = 0	#
		self.asPath = []

	def setBgpInfo(self, origin, weight, length, metric, prefix, nexthop, \
			localPreference, asPath):
		self.origin, self.weight, self.length = origin, weight, length
		self.med, self.prefix, self.nextHop = metric, prefix, nextHop
		self.localPreference, self.asPath = localPreference, asPath

	def getOrigin(self):
		return origin

	def getWeight(self):
		return weight

	def getLength(self):
		return self.length

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

	def setLength(self, length):
		self.length = length

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
		print "Origin:{}, Weight:{}, Length:{}, Metric:{}, Prefix:{}, \
			NextHop:{}, LocalPreference:{}, AsPath:{}".format(self.origin, \
			self.weight, self.length, self.med, self.prefix, self.nextHop, \
			self.localPreference, self.asPath)