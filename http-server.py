#!/usr/bin/env python3.8

import socket
import datetime
IP, PORT = '0.0.0.0', 8820

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)

while True:
    print("Connecting to a client...")
    con, addr = server.accept()
    print("Connection found from %d", addr)

    try:
        request_packet = con.recv(1024).decode()
        respone_packet = ''
        path = '\\'
        header = request_packet.split('\n')

        title = header[0]
        if not(title.startswith('GET') and title.endswith('HTTP/1.1\r')):
            con.send(b'HTTP/1.1 400 Bad Request')
            break

        respone += 'HTTP/1.1 200 OK\r\n'
        
        url = title.split(' ')[1]
        if url.endswith('txt') or url.endswith('html'):
            respone_packet += 'Content-Type: text/html; charest=utf-8\r\n'
        elif url.endswith('jpg'):
            respone_packet += 'Content-Type: image/jpg\r\n'
        elif url.endswith('js'):
            respone_packet += 'Content-Type: text/javascript; charest=utf-8\r\n'
        elif url.endswith('css'):
            respone_packet += 'Content-Type: text/css\r\n'
            
        respone_packet += 'X-Cloud-Trace-Context: cdb7a6e0394dc92c4b097cee10f2b727;o=1\r\n'
        
        h = str(datetime.datetime.now())[:-7] + ' GMT\r\n'
        respone_packet += h
        
        respone_packet += 'Server: Google Frontend\r\n'
            
        if url == '':
            path = 'C:\\weboot\\index.html'
        else:
            path = 'C:\\webroot\\' + '\\'.join(url.split('/'))

        data = open(path).read()
        respone_packet += 'Content-Length: ' + str(len(data)) + '\r\n'
        
        respone_packet += data

        con.send(respone_packet.encode())

    except:
        con.send(b'HTTP/1.1 404 Not Found\r\n')

con.close()
server.close()
