#WARNING: This proxy can't work on HTTPS websites
from os import add_dll_directory, truncate
import socket
import sys
import ssl

HOST = 'localhost'
PORT = 8088

if len(sys.argv) <= 1:
    print('Usage: "python server.py server_ip"\nserver_ip: It is the IP Address of Proxy Server')
    sys.exit(2)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen()
print("Server is listening on port " + str(PORT))
while True:
    print('Ready to server...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(10244400)
    # print(message)
    targetAddrLine = message.decode().split("\n")[0]
    print("addstart---")
    # print(targetAddrLine)
    if (targetAddrLine != ''):
        targetAddr = targetAddrLine.split(' ')[1]
        targetAddr = targetAddr.replace("http://", "", 1)
        targetAddr = targetAddr.replace("www.", "", 1)
        if ('/' in targetAddr):
            targetAddr = targetAddr.split('/')[0]
        if (':' in targetAddr):
            targetAddr = targetAddr.split(':')[0]
        print(targetAddr)
        print("addstop------")


        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((targetAddr, 80))
        conn.send(message)
        rq = conn.recv(300000000)
        tcpCliSock.send(rq)
        # print(rq)
    # # print("------")
    # # print(message.split()[1]) 
    # filename = message.split()[1]
    # if '//' in filename:
    #     filename = filename.partition("/")[2]
    # # print(filename.replace("www.","",1))

    # c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # c.bind(("localhost", 8089))

    # hostn = filename.replace("www.", "", 1)
    # hostn = hostn.split(":")[0]
    # hostn = hostn.replace(".vn", "", 1)
    # print("Hostname: " + hostn)
    # c.connect((hostn, 80))
    # res = c.recv(4096)
    # print(res.decode())