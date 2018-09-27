from socket import *
import sys
from threading import *
import os
from select import select
import datetime
import _thread


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
    count = 0
    while True:
        sentence = conn.recv(1024).decode()
        cap_sentence = sentence.upper()
        if cap_sentence == 'HELO':
            count += 1
            responce = 'hello'
            responce.strip('HELO')
            conn.send(responce.encode())
        elif 'MAIL FROM' in cap_sentence and count == 1:
            count += 1
            responce = '250 OK'
            mailfrom = cap_sentence
            mailfrom = mailfrom[10:]
            conn.send(responce.encode())
        elif 'RCPT TO' in cap_sentence and count == 2:
            count += 1
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
        elif cap_sentence == 'DATA' and count == 3:
            count += 1
            responce = '354 Send message content; End with <CLRF>.<CLRF>'
            conn.send(responce.encode())
            date = 'Date: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            files = os.listdir(current_directory)               #----START new email creation
            max_mtime = 0                                       #----sets last modified file to 0
            if len(files) != 0:                                 #----check for empty dir
                for fname in files:                             #----loop to grab last modified file
                    mtime = os.path.getmtime(current_directory) #----
                    if mtime > max_mtime:                       #----
                        email = fname                           #----
                    last = email.split('.')[0]                  #----makes a new file if dir is empty
                    emailfile = email.split('.')[1]             #----
                    last = int(last) + 1                        #----
                    emailfile = '00' + str(last) + '.' + emailfile #----
            else:                                               #----
                emailfile = '001.email'                         #----END new email creation
            body = 'Subject: '
            data = conn.recv(1024).decode()
            body = data
            filepath = os.path.join(current_directory, emailfile)
            f = open(filepath, "a")             #---- START writes content to the new email file
            f.write(date + '\n')                #---- write date
            f.write('From: ' + mailfrom + '\n') #---- write who from
            f.write('To: ' + reciever + '\n')   #---- write to
            f.write('Subject: ' + body)         #---- write body
            f.close()                           #---- END close file
            responce = '250 OKAY'
            conn.send(responce.encode())
        elif cap_sentence == 'QUIT':
            responce = '221 Bye'
            conn.send(responce.encode())
            conn.close()
        else:
            responce = '500 Command invalid or protocol command out of order. \n Start from helo.'
            count = 0
            conn.send(responce.encode())




    conn.close()



##################################
# UDP connection thread
##################################
def UDP_connect(udp_listen_port):
    message, clientAddress = udp.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    if 'GET' in modifiedMessage:                #----START Get request
        msg = modifiedMessage.split('/')        #----split msg to ID user
        user = msg[2]                           #----init user
        count = modifiedMessage.split('COUNT:') #----Split count to know how many emails to retrieve
        count = int(count[1])                   #----convert string to int
                                                #----END GET request
        mail_directory = os.getcwd()                                #----current dir path
        mail_directory = os.path.join(mail_directory+'/db/'+user)   #----add to user dir to current path                              
        if not os.path.exists(mail_directory):                      #----checks if user is in DB
            responce = '404: File path not found.'
            udp.sendto(responce.encode(), clientAddress)
        else:
            files = os.listdir(mail_directory)                      #----grabs emails of the user
            files = sorted(files) 
            files = reversed(files)
            files = list(files)
            current_directory = os.getcwd()
            i = 0
            while i < count and count < len(files):             #----START writing emails to txt files
                message = ''                                    #----
                mail = files[i]                                 #----
                filepath = os.path.join(mail_directory, mail)   #----
                f = open(filepath, 'r')                         #----
                message = f.read()                              #----
                f.close()                                       #----
                mail = mail.split('.')[0]                       #---- 
                mail = mail + '.txt'                            #----
                storepath = os.path.join(current_directory,mail)#----
                m = open(storepath, 'a')                        #----
                m.write(message)                                #----
                f.close()                                       #----END closes txt files
                i += 1
    else: 
        print('Invalid GET request')
    modifiedMessage = "Check current directory for text file"
    udp.sendto(modifiedMessage.encode(), clientAddress)


udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(('', udp_listen_port))

tcp = socket(AF_INET, SOCK_STREAM) 
tcp.bind(('',int(arg_list[1])))
tcp.listen(5)



input = [tcp,udp]
while True:
    inputready,outputready,exceptready = select(input,[],[])

    for s in inputready:
        if s == tcp:
            conn, addr = tcp.accept()
            #threadTCP = Thread(target = clientthread(conn,tcp_listen_port)).start()
            #threadTCP.start()
            _thread.start_new_thread(clientthread ,(conn,tcp_listen_port))

        elif s == udp:
            threadUDP = Thread(target = UDP_connect(udp_listen_port))
            threadUDP.start()

        else:
            print ("unknown socket:", s)
