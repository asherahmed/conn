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
def clientthread(conn1,conn2,me1,selection):
    global a
    global b
    global c
    j=0
    #Sending message to connected client

    conn1.send('Welcome to the Server. Type conn if you want to send request\n') #send only takes string

    while True:	
    	command1= conn1.recv(1024)
	if command1 == 'y' or command1 == 'conn':
		break
    if command1 == 'conn' :
    	conn1.send('Available Users are:')
    	while True:
		if j>=len(b):
			break
		if a[j]== me1:
			j=j+1
		if a[j] in b.keys():
			conn1.send(a[j])
			conn1.send('\n')
		j=j+1
    	conn1.send('Select one:\n')
    	while True:
    		selection= conn1.recv(1024)
		if b.has_key(selection):
    			conn2 = b[selection]
			conn2.send('Getting Request from '+ str(me1) + ' : ')
			c[selection]= me1
			break
				
		else:
			conn1.send('No Such Connection found. Try Again\n')

    elif command1 == 'y':
	selection = c[me1]
	conn2 = b[selection]
	     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn1.recv(1024)
        if not data: 
            break
	print 'Received from '+ str(me1) + ': ' + str(data)

	print 'Sending to '+ str(selection)
	data= str(me1)+': ' +str(data)
        conn2.sendall(data)
	
     
    #came out of loop
    conn1.close()
 
#now keep talking with the client
conn = [0,0,0,0,0,0,0,0,0,0]
a= ['Asher', 'Saad','Fahad', 'Hassan', 'Abdul Raheem', 'Sir Tahir', 'Nauman', 'Rabee', 'Tuseeq', 'Ali']
b={}
c={}
for i in range(10):
    #wait to accept a connection - blocking call
    conn[i], addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    conn[i].send('Your Name:')
    a[i]= conn[i].recv(1024)
    b[a[i]] = conn[i]
    
	
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn[i],None,a[i],None))
 
s.close()
