#!/usr/bin/env python3
"""
	Allan Millar
	Program for testing #1
    Client
"""

import sys
import socket
import time

#command = str(sys.argv[1])

host = "127.0.0.1"


with socket.socket(socket.AF_INET, 
    socket.SOCK_STREAM
    ) as socket:
    socket.connect((host, 12345))

    while True:
        time.sleep(1)
        usr_input = input("Enter the command: ")
        if (usr_input=="exit"):
            print("If block")
            break
        elif (usr_input=="disconnect"):
            print("Elif block #1")
            data = "Close connection"
            socket.sendall(data.encode())
            data = socket.recv(1024)
            print("Recieved", repr(data.decode()))
        elif (usr_input=="shut down"):
            print("Elif block #2")
            data = "Shut off server"
            socket.sendall(data.encode())
            data = socket.recv(1024)
            print("Recieved", repr(data.decode()))
        else:
            print("Else block")
            data = "Generic response"
            socket.sendall(data.encode())
            data = socket.recv(1024)
            print("Recieved", repr(data.decode()))
"""

for id in range (5):
    with socket.socket(socket.AF_INET, 
        socket.SOCK_STREAM
        ) as socket:
        socket.connect((host, 12345))
        
        time.sleep(id*5)
        socket.sendall(command.encode())
        data = socket.recv(1024)
        print("Recieved", repr(data.decode()))


    data = "This specific arrangment of letters."
    socket.sendall(data.encode())
    data = socket.recv(1024)
    print("Recieved", repr(data.decode()))
"""

sys.exit(0)