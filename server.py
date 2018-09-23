from socket import *
import sys
from threading import Thread
import os 
from select import select
import datetime
import errno
from time import sleep

################################################
# Gets current file path and creates a 'db' file
################################################
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'db')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

#####################
# argv specifications
#####################
arg_list = sys.argv
tcp_listen_port = int(arg_list[1])
udp_listen_port = int(arg_list[2])

if len(arg_list) != 3:
    print('Usage: python3 server.py <TCP-listen-port> <UDP-listen-port>')

########################
# TCP client thread
########################
def clientthread(conn,port):
    print('Server is ready to recieve TCP.')

    while True:
        print('here')
        sentence = conn.recv(1024).decode()
        cap_sentence = sentence.upper()
        if cap_sentence == 'HELO':
            responce = 'hello'
            responce.strip('HELO')
            conn.send(responce.encode())
        elif 'MAIL FROM' in cap_sentence:
            responce = '250 OK'
            mailfrom = cap_sentence
            mailfrom = mailfrom[10:]
            conn.send(responce.encode())
        elif 'RCPT TO' in cap_sentence:
            responce = '250 OK'
            rcptto = cap_sentence 
            reciever = cap_sentence  
            reciever = reciever[8:]             #----START used the email in rcpt to 
            rcptto = rcptto[8:]                 #----to create and new email dir
            rcptto = rcptto.split('@')[0]       #----if one does not exist
            current_directory = os.getcwd()     #----
            current_directory = os.path.join(current_directory+'/db/'+rcptto) #----
            if not os.path.exists(current_directory): #----
                os.makedirs(current_directory)  #----END dir creation
            conn.send(responce.encode())
        elif cap_sentence == 'DATA':
            responce = '354 Send message content; Format for message\n'
            responce = responce + 'Subject: XXXxxxXXX\n'
            responce = responce + '<body>\n'
            responce = responce + 'After <body> is complete clear the line. End with <CLRF>.<CLRF>'
            conn.send(responce.encode())
            date = 'Date: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            files = os.listdir(current_directory)               #----START new email creation
            max_mtime = 0                                       #----sets last modified file to 0
            if len(files) != 0:                                 #----check for empty dir
                for fname in files:                             #----loop to grab last modified file
                    mtime = os.path.getmtime(current_directory) #----
                    if mtime > max_mtime:                       #----
                        email = fname                           #----
            else:                                               #----
                email = '001.email'                             #----makes a new file if dir is empty
            last = email.split('.')[0]                          #----
            emailfile = email.split('.')[1]                     #----
            last = int(last) + 1                                #----
            emailfile = '00' + str(last) + '.' + emailfile      #----END new email creation
            body = 'Subject: '
            while 1:                            #----START loop for email content
                data = conn.recv(1024).decode() #----
                body = (body + data + '\n')     #----
                dataresp = ' '                  #----
                conn.send(dataresp.encode())    #----
                if data == '.':                 #----
                    break                       #----END loop for email content
           
            filepath = os.path.join(current_directory, emailfile) 
            f = open(filepath, "a")             #---- START writes content to the new email file
            f.write(date + '\n')                #---- write date
            f.write('From: ' + mailfrom + '\n') #---- write who from
            f.write('To: ' + reciever + '\n')   #---- write to
            f.write(body)                       #---- write body
            f.close()                           #---- END close file
            responce = '250 OKAY'
            conn.send(responce.encode())
        elif cap_sentence == 'QUIT':
            responce = '221 Bye'
            conn.send(responce.encode())
            conn.shutdown(1)
            conn.close()
            sys.exit()
        else:
            responce = 'Invalid command'
            conn.send(responce.encode())
            
           


    conn.close()

    

##################################
# UDP connection thread
##################################
def UDP_connect(udp_listen_port):
    print('The server is ready to recieve UDP.')
    while True:
        message, clientAddress = udp.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        print('hey')
        if modifiedMessage == 'HELO':
            responce = 'helo'
            udp.sendto(responce.encode(), clientAddress)
        elif modifiedMessage == 'MAIL FROM':
            responce = 'mail from'
            udp.sendto(responce.encode(), clientAddress)
        elif modifiedMessage == 'RCPT TO':
            responce = 'rcpt to'
            udp.sendto(responce.encode(), clientAddress)
        elif modifiedMessage == 'DATA':
            responce = 'data'
            udp.sendto(responce.encode(), clientAddress)
        elif modifiedMessage == 'QUIT':
            responce = 'quit'
            udp.sendto(responce.encode(), clientAddress)
        else:
            pass

        
    udp.sendto(modifiedMessage.encode(), clientAddress)

udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(('', udp_listen_port))

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('',int(arg_list[1])))
tcp.listen(1)



input = [tcp,udp]
while True:
    inputready,outputready,exceptready = select(input,[],[])

    for s in inputready:
        if s == tcp:
            conn, addr = tcp.accept()   
            threadTCP = Thread(target = clientthread(conn,tcp_listen_port))
            threadTCP.start()   
            
        elif s == udp:
            threadUDP = Thread(target = UDP_connect(udp_listen_port))
            threadUDP.start()
            
        else:
            print ("unknown socket:", s)
