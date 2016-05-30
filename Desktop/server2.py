'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *



HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5189 # Arbitrary non-privileged port
 
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
def clientthread(conn1,conn2,me1,selection,i):
    global a
    global b
    global c
    j=0
    #Sending message to connected client

    conn1.send('Welcome to the Server. Type Msg with Name: if you want to send request\n') #send only takes string

    while True:	
    	command1= conn1.recv(1024)
	if c.get(me1,'') or ':' in command1:
		break
    if ':' in command1:
	selection= command1[:command1.find(':')]
	if b.has_key(selection):
		conn2 = b[selection]
		conn2.send(str(me1) + ': ' +command1[command1.find(':')+1:])
		c[selection]= me1
				
	else:
		print selection
		conn1.send('No Such Connection found. Try Again\n')

    elif c.get(me1,''):
	selection = c[me1]
	conn2 = b[selection]
	conn2.send(str(me1) + ': ' +command1[command1.find(':')+1:])
	     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn1.recv(1024)
        if ':' in data:
	    selectold= selection

	    selection= data[:data.find(':')]
	    if b.has_key(selection):
		del c[selectold]
		conn2 = b[selection]
		conn2.send(str(me1) + ': ' +data[data.find(':')+1:])
		c[selection]= me1
		continue

	    else:
		selection = selectold

        elif c.get(me1,''):
	    selection = c[me1]
	    conn2 = b[selection]
	    conn2.send(str(me1) + ': ' +data[data.find(':')+1:])
	    continue
	if data == 'list':
	    j=0
	    while True:
		if j>=10:
			break
		if a.get(j,''):
			if a[j] in b.keys():
				conn1.send(a[j])
				conn1.send('\n')
		j=j+1
	    continue
        if not data: 
            break
	if data == 'quit':
	    if me1 in c.keys():
	    	del c[me1]
	    del b[me1]
	    del a[i]
	    conn1.close()
            break
	print 'Received from '+ str(me1) + ': ' + str(data)

	print 'Sending to '+ str(selection)
	data= str(me1)+': ' +str(data)
        conn2.sendall(data)
	
     
    #came out of loop

 
#now keep talking with the client
conn = [0,0,0,0,0,0,0,0,0,0]
a= {}
b={}
c={}
for i in range(10):
    #wait to accept a connection - blocking call
    conn[i], addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    conn[i].send('Your Name:')
    a[i]= conn[i].recv(1024)
    b[a[i]] = conn[i]
    j=0
    
    while True:
	if j>i:
	    break
	k=0
	while True:
		if k>10:
		    break
		if a.get(k,''):
			if a.get(k,'') in b.keys():
	    	 	   conn[j].send(a[k])
	    	 	   conn[j].send('\n')
		k=k+1
	j=j+1
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn[i],None,a[i],None,i))
 
s.close()
