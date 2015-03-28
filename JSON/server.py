import SocketServer
import json

class MyTCPServer(SocketServer.ThreadingTCPServer):
		allow_resue_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
		def handle(self):
			try:
				data = json.loads(self.request.recv(1024).strip())

				print data

				#self.request.sendall(json.dumps({'return':'ok'}))
			except Exception, e:
				print "Exception while receiving message: ", e
server = MyTCPServer(('127.0.0.1', 13373), MyTCPServerHandler)
server.serve_forever()