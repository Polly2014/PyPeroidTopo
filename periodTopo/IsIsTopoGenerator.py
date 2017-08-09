# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

from sqlalchemy import *
from sqlalchemy.orm import *
from db_models import *

import db_config
import networkx as nx
import plugins
import time
import json
import os
try:
    import cPickle as pickle
except:
    import pickle

class IsIsTopoGenerator(object):
	"""docstring for IsIsTopoGenerator"""
	def __init__(self):
		self.pid = ""
		self.links = []
		self.mapPrefixRouterid = {}
		
	def connectDB(self, DB_CONFIG):
		try:
			engine = create_engine('{engine}://{username}:{password}@{address}:{port}/{database}?charset=utf8'.format(**DB_CONFIG), echo=False)
			DB_Session = sessionmaker(bind=engine)
			self.session = DB_Session()
			print "DataBase connect successful!"
		except:
			print "DataBase connect failed..."

	def disconnectDB(self):
		try:
			self.session.commit()
			self.session.close()
			print "DataBase disconnect successful!"
		except:
			print "DataBase disconnect failed..."

	def makeIsIsTopo(self, periodID=""):
		self.pid = periodID
		pTime = plugins.pidToStamp(self.pid)

		isis_link_set = self.session.query(IsisLinkInfo).filter( \
			IsisLinkInfo.create_time<=pTime, IsisLinkInfo.end_time>pTime)
		isis_router_set = self.session.query(IsisRouterReachability).filter( \
			IsisLinkInfo.create_time<=pTime, IsisLinkInfo.end_time>pTime)

		# Step One: Make Nodes Info
		for router in isis_router_set.all():
			self.addPrefixRouterid(router.prefix, router.sys_id)

		# Step Two: Make Links Info
		for link in isis_link_set.all():
			l = (link.sys_id, link.n_sys_id, link.metric)
			self.addLink(l)
		for l in self.links:
			print "### {}->{} [{}]".format(l[0], l[1], l[2])


	def addPrefixRouterid(self, prefix, routerId):
		self.mapPrefixRouterid[prefix] = routerId

	def getRouteridByPrefix(self, prefix):
		return self.mapPrefixRouterid[prefix]

	def addLink(self, link):
		if link not in self.links:
			self.links.append(link)

	def getShortestPaths(self, srcSeg, dstSeg, srcRouterId, dstRouterId):
		result = {"code":0, "message":""}
		g = nx.DiGraph()
		edges = self.links
		g.add_weighted_edges_from(edges)
		try:
			#s, t = map(self.getRouteridByPrefix, [srcSeg, dstSeg])
			s, t = srcRouterId, dstRouterId
		except:
			result["message"] = "Start or End Router Found Error..."
			return result
		print "Source:{} -> Target:{}".format(s,t)
		if s==t:
			result["code"] = 1
			result["message"] = [[s]]
			return result
		try:
			paths = nx.all_shortest_paths(G=g, source=s, target=t, weight="weight")
			result["code"] = 1
			result["message"] = list(paths)
		except Exception, e:
			result["message"] = "Path Found Error: {}-{}".format(Exception, e)
		return result

def test():
	t = IsIsTopoGenerator()
	t.connectDB(db_config.DB_CONFIG)
	t.makeIsIsTopo("201707282039")
	print t.getShortestPaths("192.168.1.0", "192.168.5.0")

# test()