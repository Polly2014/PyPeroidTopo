#-*-coding:utf-8-*-

from sqlalchemy import *
from sqlalchemy.orm import *
from db_models import *
from db_config import DB_CONFIG

import networkx as nx
import plugins
import time


#--------------------DataBase Connect Start------------------------#
engine = create_engine('{engine}://{username}:{password}@{address}:{port}/{database}?charset=utf8'.format(**DB_CONFIG), echo=False)

DB_Session = sessionmaker(bind=engine)

session = DB_Session()
#session.commit()

#--------------------DataBase Query Start------------------------#
ospf_link_set = session.query(HzOspfLinkInfo)
ospf_lsa_set = session.query(HzOspfAsexternallsa)
bgp_link_set = session.query(BgpLinkInfo)


#--------------------AS Topo Generation Start------------------------#
# Step One: Get the whole as_num
as_num_list = [l.as_num for l in ospf_link_set.group_by(HzOspfLinkInfo.as_num).all()]
print as_num_list
# Step Two: Make The Topo for Each AS
as_graph_list = []
for as_num in as_num_list:
	as_graph = nx.DiGraph(as_num=as_num)
	link_set = ospf_link_set.filter(HzOspfLinkInfo.as_num==as_num, \
		or_(HzOspfLinkInfo.link_type==2,HzOspfLinkInfo.link_type==1)).all()
	edges = plugins.makeGraphEdges(link_set)
	as_graph.add_weighted_edges_from(edges)
	try:
		print nx.shortest_path_length(as_graph, weight='weight')
	except:
		pass
	#print as_graph.graph
	#print as_graph.number_of_edges()
	print "_________________________________"
	#print link_set








#print unique([l.as_num for l in links])

# periodid = int(time.time())
# print periodid

# print type(HzOspfLinkInfo)
# print "----------------------"
# print type(t_view_ospf_link_info)
# print mapper(HzOspfLinkInfo, t_view_ospf_link_info)
#print session
# HzOspfLinkInfo t_view_ospf_link_info
# query = session.query()
# print query.count()