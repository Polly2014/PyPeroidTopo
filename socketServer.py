# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import threading
import SocketServer
from socketConfig import socketConfig
import json
from periodTopo.HzOspfTopoGenerator import HzOspfTopoGenerator
from periodTopo.OspfTopoGenerator import OspfTopoGenerator
from periodTopo.IsIsTopoGenerator import IsIsTopoGenerator
from analyser.RouteAnalyser import RouteAnalyser

sc = socketConfig()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def setup(self):
        ip = self.client_address[0].strip()     # 获取客户端的ip
        port = self.client_address[1]           # 获取客户端的port
        print(ip+":"+str(port)+" is connect!")

    def handle(self):
        data = self.request.recv(1024).strip()
        cur_thread = threading.current_thread()
        client_address = self.client_address
        response = "{}:Recieved from{}-{}".format(cur_thread.name, client_address, data)
        print response

        query = json.loads(data)
        protocol = sc.getProtocol()

        if protocol=="ospf":
            print "ospf Processing..."
            self.ospfProcessing(query)
        elif protocol=="isis":
            print "isis Processing..."
            self.isisProcessing(query)
        else:
            pass

        # pid = query.get("pid")
        # srcIp, dstIp = query.get("srcIp"), query.get("dstIp")
        # srcMask, dstMask = query.get("srcMask"), query.get("dstMask")
        # srcAs, dstAs = query.get("srcAs"), query.get("dstAs")

        # t = HzTopoGenerator(pid)
        # t.connectDB(sc.getDBConfig())
        # t.makeHzTopo()
        
        # r = RouteAnalyser()
        # result = r.getOverallRoute(pid, srcIp, dstIp, srcMask, dstMask, srcAs, dstAs)
        # print result
        # self.request.sendall(json.dumps(result))

    def ospfProcessing(self, query):
        isHQ = sc.judgeHQ
        pid = query.get("pid")
        srcIp, dstIp = query.get("srcIp"), query.get("dstIp")
        srcMask, dstMask = query.get("srcMask"), query.get("dstMask")
        srcAs, dstAs = query.get("srcAs"), query.get("dstAs")
        if isHQ:
            t = HzOspfTopoGenerator()
            t.connectDB(sc.getDBConfig())
            t.makeHzTopo(pid)
            
            r = RouteAnalyser()
            result = r.getOverallRoute(pid, srcIp, dstIp, srcMask, dstMask, srcAs, dstAs)
            print result
        else:
            t = OspfTopoGenerator()
            t.connectDB(sc.getDBConfig())
            t.makeOspfTopo(pid)
            result = t.getShortestPaths(srcIp, dstIp)
        self.request.sendall(json.dumps(result))


    def isisProcessing(self, query):
        pid = query.get("pid")
        srcIp, dstIp = query.get("srcIp"), query.get("dstIp")
        t = IsIsTopoGenerator()
        t.connectDB(sc.getDBConfig())
        t.makeIsIsTopo(pid)
        result = t.getShortestPaths(srcIp, dstIp)
        self.request.sendall(json.dumps(result))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port

    server = ThreadedTCPServer(sc.getHostPort(), ThreadedTCPRequestHandler)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever())
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    # while True:
    #     pass
    # else:
    #     server.shutdown()
    #     server.server_close()