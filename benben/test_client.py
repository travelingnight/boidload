#!/usr/bin/env python3
"""
	Allan Millar
	Program for testing #1
    Client
"""

import sys
import socket
import time

PORT = int(sys.argv[1])

IP = sys.argv[2]

def launch_client(PORT, IP):
    with socket.socket(socket.AF_INET, 
        socket.SOCK_STREAM
    ) as sock:
        sock.connect((IP, PORT))
        
        while True:
            time.sleep(1)
            data = sock.recv(1024)
            if len(data) == 0:
                break
            print("Recieved", repr(data.decode()))
            #sock.sendall(data.encode())
    return

def main():

    launch_client(PORT, IP)
    
    sys.exit(0)

if __name__ == "__main__":
    main()