#-*-coding:utf-8-*-

from sqlalchemy import *
from sqlalchemy.orm import *
from db_models import *
#from db_config import DB_CONFIG

import networkx as nx
import db_config
import plugins
import time
import json
import os
try:
    import cPickle as pickle
except:
    import pickle

class HzTopoGenerator():
    
    def __init__(self, periodID=''):
        self.pid = periodID
        self.session = ""
        self.hzTopo = []
        self.topoFilePathName = "topoFile/"
        #self.topoFilePathName = "../topoFile/"

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

    def makeHzTopo(self):
        self.topoFilePathName += "ospf-{}.pkl".format(self.pid)
        if os.path.exists(self.topoFilePathName):
            print "OspfFile Already exists!"
            self.disconnectDB()
            return
        pTime = plugins.pidToStamp(self.pid)

        ospf_link_set = self.session.query(HzOspfLinkInfo).filter( \
            HzOspfLinkInfo.create_time<=pTime,HzOspfLinkInfo.end_time>pTime)
        ospf_lsa_set = self.session.query(HzOspfAsexternallsa)
        bgp_link_set = self.session.query(BgpLinkInfo)
        bgp_path_set = self.session.query(HzBgpPathInfo).filter( \
            HzOspfLinkInfo.create_time<=pTime,HzOspfLinkInfo.end_time>pTime)
        
        # Step One: Get the whole as_num
        as_num_list = [l.as_num for l in ospf_link_set.group_by(HzOspfLinkInfo.as_num).all()]

        for as_num in as_num_list:
            # Step Two-1: Make Neighbors Object
            tmpSet = ospf_link_set.filter(HzOspfLinkInfo.as_num==as_num, \
                HzOspfLinkInfo.link_type.in_((1,2))).all()
            routerNeighbors = {}
            for t in tmpSet:
                neighbor = {
                    "id": t.id, "area": t.area_id, "interfaceIP": t.interface_ip, 
                    "mask": t.mask, "nRouterId": t.n_router_id, "metric": t.metric}
                if routerNeighbors.has_key(t.router_id):
                    routerNeighbors[t.router_id].append(neighbor)
                else:
                    routerNeighbors[t.router_id] = [neighbor]
                # neighbors.append({
                #     "id": t.id, "area": t.area_id, "interfaceIP": t.interface_ip, 
                #     "mask": t.mask, "nRouterId": t.n_router_id, "metric": t.metric})
            
            # TODO: 双边检测

            # Step Two-2: Make Nodes Object
            nodes = []
            for routerId, neighbors in routerNeighbors.items():
                #print "routerId:{}\nneighbors:{}".format(routerId, neighbors)
                nodes.append({"routerId": routerId, "neighbors": neighbors})

            # Step Two-3: Make Stubs Object
            tmpSet = ospf_link_set.filter(HzOspfLinkInfo.as_num==as_num, \
                HzOspfLinkInfo.link_type==3).all()
            stubs = []
            for t in tmpSet:
                stubs.append({
                    "routerId":t.router_id, "prefix":plugins.prefixByIpMask(t.interface_ip,t.mask),
                    "mask":t.mask})

            # Step Two-4: Make InterLinks Object
            tmpSet = ospf_link_set.filter(HzOspfLinkInfo.as_num==as_num, \
                HzOspfLinkInfo.link_type==11).all()
            interLinks = []
            for t in tmpSet:
                interLinks.append({
                    "linkId":t.id, "routerId":t.router_id, "interfaceIP":t.interface_ip,
                    "nRouterId":t.n_router_id, "nAsNumber":t.n_as_num, "mask":t.mask,
                    "metric":t.metric})

            # Step Two-5: Make OuterInfo Object
            tmpSet = bgp_path_set.filter(HzBgpPathInfo.as_num==as_num)
            bgp = []
            for t in tmpSet:
                aspath = ""
                bgp.append({
                    "prefix":t.networkNum, "length":t.prefixLen, "nexthop":t.nextHop,
                    "weight":t.weight, "origin":t.origin, "localPreference":t.local_pref,
                    "med":t.med, "aspath":aspath})
            tmpSet = ospf_lsa_set.filter(HzOspfAsexternallsa.as_num==as_num, \
                HzOspfAsexternallsa.isUseful==1)
            lsa = []
            for t in tmpSet:
                lsa.append({
                    "advRouter":t.adRouter, "linkStateId":t.linkStateID,
                    "networkMask":t.networkMask, "externalType":t.externalType,
                    "metric":t.metric, "forwardingAddress":t.forwardAddress})
            outerInfo = {"BGP":bgp, "ExternalLsa":lsa}
            
            # Step Two-6: Integration
            topo = {"InterLink":interLinks, "stubs":stubs, "nodes":nodes}
            self.hzTopo.append({"asNumber":as_num,"Topo":topo,"OuterInfo":outerInfo})
        self.disconnectDB()
        self.writeTopoToDisk()


    def writeTopoToDisk(self):
        with open(self.topoFilePathName, 'wb') as f:
            pickle.dump(self.hzTopo, f)
            #json.dump(self.hzTopo, f, indent=4)
            #f.write(json.dumps(self.hzTopo))

    def getTopoFilePathName(self):
        return self.topoFilePathName

    def makeHzTopoFile(self):
        pass
def test():
    t = HzTopoGenerator("201707282039")
    t.connectDB(db_config.DB_CONFIG)
    t.makeHzTopo()
    print t.hzTopo

#test()