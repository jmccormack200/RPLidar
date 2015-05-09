import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World"

print "UDP target IP: ", UDP_IP
print "UDP target Port: ", UDP_PORT
print "message: ", MESSAGE

sock = socket.socket(socekt.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
