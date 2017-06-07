#-*-coding:utf-8-*-

from IPy import IP
import time

class Node(object):
	def __init__(self, router_id):
		self.router_id = router_id
	def __repr__(self):
		return "%s"%self.router_id


unique = lambda l: list(set(l))

def makeGraphEdges(link_set):
	result = []
	for link in link_set:
		srcNode = link.router_id
		dstNode = link.n_router_id
		weight = link.metric
		result.append((srcNode, dstNode, weight))
	return result

def makeGraphEdge(link):
	srcNode = Node(link.router_id)
	dstNode = Node(link.n_router_id)
	weight = link.metric
	return (srcNode, dstNode, weight)

def pidToSystemTime(peroidID):
	pass

def prefixByIpMask(ip, mask):
	return IP(ip).make_net(mask).int()

def pidToStamp(pid):
	return time.mktime(time.strptime(pid, "%Y%m%d%H%M"))



longToIP = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])
ipToLong = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
