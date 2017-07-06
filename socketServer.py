# -*- coding:utf-8 -*-
# @Date    : 2017-06-08 00:12:47
# @Author  : Polly
# @Email   : wangbaoli@ict.ac.cn
# @Version : 1.0.0

import threading
import SocketServer

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
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

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