#!/usr/bin/python
from socket import*
import json

HOST = 'xxx.xxx.xxx.xxx'
PORT = 4998

if __name__ == "__main__":
    with open('irrawcode.json', 'r') as f:
        keys=json.load(f)
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    tcpCliSock.send(keys['open'].encode())
    data = tcpCliSock.recv(BUFSIZE).decode()
    print(data)
    tcpCliSock.close()
