import socket

UDP_IP = "192.168.0.111"
UDP_PORT = 2390
MESSAGE = "10"

print "UDP target IP: ", UDP_IP
print "UDP target Port: ", UDP_PORT
print "message: ", MESSAGE

for a in range(0, 10):
	MESSAGE_SENT = MESSAGE
	print a
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(MESSAGE_SENT, (UDP_IP, UDP_PORT))
