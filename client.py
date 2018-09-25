from socket import *

serverName = '127.0.0.1'
tcpserverPort = 12000
udpserverport = 10000
print('Would you like to send or recieve?')
sendOrRecieve = input()
if sendOrRecieve == 'send':
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, tcpserverPort))
elif sendOrRecieve == 'recieve':
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    #message = input('Send a get request.\n')
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    message = '\n'.join(lines)
    print(message)
    clientSocket.sendto(message.encode(),(serverName,udpserverport))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
else:
    print('invalid selection')


while 1:
    msg = input()
    clientSocket.send(msg.encode())
    modifiedsentance = clientSocket.recv(1024)
    
    print('From server: ', modifiedsentance.decode())

clientSocket.close()