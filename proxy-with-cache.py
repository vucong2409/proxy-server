#WARNING: This proxy can't work on HTTPS websites
from os import add_dll_directory, truncate
import socket
import sys
import ssl

HOST = 'localhost'
PORT = 8088

def transformCacheName(linkAddr):
    result = linkAddr
    result = result.replace('https://', '')
    result = result.replace('http://', '')
    result = result.replace('/', '-slash-')
    result = result.replace('~', '-tilde-')
    result = result.replace(':443', '')
    return result
    

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen()
print("Server is listening on port " + str(PORT))
print('Ready to serve...')
while True:
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(10244400)
    # print(message)
    targetAddrLine = message.decode().split("\n")[0]
    print("addstart---")
    cachename = targetAddrLine.split(" ")[1]
    try: 
        cacheFile = open('./cache/' + transformCacheName(cachename), 'rb')
        byte = cacheFile.read()
        # print(byte)
        tcpCliSock.send(byte)
        tcpCliSock.close()
        cacheFile.close()
    except IOError:
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
            newCacheFile = open('./cache/' + transformCacheName(cachename), 'wb')
            newCacheFile.write(rq)
            newCacheFile.close()
            tcpCliSock.send(rq)
            tcpCliSock.close()
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