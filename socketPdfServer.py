# -*- coding:utf-8*-
import threading

import socket
import time

encoding = 'utf-8'

BUFSIZE = 1024

from printSheet import *

# 是否停止
isStop = False


# a read thread, read data from remote

class Reader(threading.Thread):

    def __init__(self, client):

        threading.Thread.__init__(self)

        self.client = client

    def run(self):

        # while True:
        global isStop
        data = self.client.recv(BUFSIZE)

        if (data):
            cacheKey = bytes.decode(data, encoding)
            # 关闭socket
            if (cacheKey == 'exitListener'):
                self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                isStop = True
                print "收到停止信号，停止监听"
            else:
                print cacheKey
                PS = printSheet()
                result = PS.create(cacheKey)
                print "from client::", result, ""

                self.client.send(result)

        # print "close:", self.client.getpeername()

    def readline(self):

        rec = self.inputs.readline()

        if rec:

            string = bytes.decode(rec, encoding)

            if len(string) > 2:

                string = string[0:-2]

            else:

                string = ' '

        else:

            string = False

        return string


# a listen thread, listen remote connect

# when a remote machine request to connect, it will create a read thread to handle

class Listener(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)

        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind(("0.0.0.0", port))

        self.sock.listen(0)

    def run(self):
        print "listener started"

        global isStop
        while isStop == False:
            client, cltadd = self.sock.accept()

            print "accept a connect..."

            Reader(client).start()

            cltadd = cltadd
            print "accept a connect(new reader..)"


import sys

number = 8888

lst = Listener(number)  # create a listen thread

lst.start()  # then start

# Now, you can use telnet to test it, the command is "telnet 127.0.0.1 9011"

# You also can use web broswer to test, input the address of "http://127.0.0.1:9011" and press Enter button

# Enjoy it....
