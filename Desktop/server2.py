'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *



HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5188 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(i):
    global conn
    a= ['Asher', 'Saad','Fahad', 'Hassan', 'Abdul Raheem', 'Sir Tahir', 'Nauman', 'Rabee', 'Tuseeq', 'Ali']
    #Sending message to connected client
    if (i%2==0):
    	conn[i].send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn[i].recv(1024)
        if not data: 
            break
	print 'Received from '+ str(a[i]) + ': ' + str(data)
	if (i%2==0):
		print 'Sending to '+ str(a[i+1])
		data= str(a[i])+': ' +str(data)
	        conn[i+1].sendall(data)
	else:
		print 'Sending to '+ str(a[i-1])
		data= str(a[i])+': ' +str(data)
	        conn[i-1].sendall(data)
     
    #came out of loop
    conn[i].close()
 
#now keep talking with the client
conn = [0,0,0,0,0,0,0,0,0,0]
for i in range(10):
    #wait to accept a connection - blocking call
    conn[i], addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(i,))
 
s.close()
