#!/usr/bin/python
from socket import*
import json

HOST = '192.168.1.4'
PORT = 4998

if __name__ == "__main__":
    with open('irrawcode_ac.json', 'r') as f:
        keys=json.load(f)
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    tcpCliSock.send((keys['poweroff']+'\\n\\r').encode())
    data = tcpCliSock.recv(BUFSIZE).decode()
    print(data)
    tcpCliSock.close()
