
import socket               # Import socket module
from thread import *

def receiveData(temp):
	while True:
		data= s.recv(1024)
		print str(data)
		if not data:
			break

s = socket.socket()         
host = socket.gethostname()
port = 5188                # Reserve a port for your service.

s.connect((host, port))
start_new_thread(receiveData, (None,))
while True:
	reply = raw_input()
	s.send(reply)
s.close                     # Close the socket when done
