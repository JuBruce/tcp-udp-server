from socket import *
import sys

#####################
# argv specifications
#####################
arg_list = sys.argv
serverName = arg_list[1]
port = int(arg_list[2])

if len(arg_list) != 3:
    print('Usage: python3 client.py <host IP> <Port number>')

################################
# begin client/server interation
################################
print('Would you like to send or recieve?')
sendOrRecieve = input()
if sendOrRecieve == 'send':
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, port))
elif sendOrRecieve == 'recieve':                #----Start UDP Interaction
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    message = '\n'.join(lines)
    print(message)
    clientSocket.sendto(message.encode(),(serverName, port))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    sys.exit()                                  #----End UDP interaction
else:
    print('invalid selection')

##################
#TCP interaction
##################
while 1:
    msg = input()
    clientSocket.send(msg.encode())
    modifiedsentance = clientSocket.recv(1024)
    if modifiedsentance.decode() == '221 Bye':
        print(modifiedsentance.decode())
        sys.exit()
    elif modifiedsentance.decode() == '354 Send message content; End with <CLRF>.<CLRF>':
        print(modifiedsentance.decode())
        datamsg = []
        i = 0
        while True:
            data = input()
            if data == '.':
                datamessage = '\n'.join(datamsg)
                clientSocket.send(datamessage.encode())
                break
            else:
                datamsg.append(data)
    else:
        print(modifiedsentance.decode())

clientSocket.close()