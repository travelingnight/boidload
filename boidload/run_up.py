#!/usr/bin/env python3
"""
	Allan M
	Program for testing
"""
import sys, random, socket
from contextlib import closing
from subprocess import Popen, PIPE

def find_socket():
    # This will only ever be run when the machine has already been
    # captured, and from the machine itself.
    HOST = "localhost"
    
    # Looking through ports randomly and testing if they are blocked
    # It is possible this is unnecessary given we have control, however
    # I am doing it so we can minimize messing with anything already
    # present on the machine.
    while True:
        PORT = random.randint(10000,65535)
        with closing(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ) as sock:
            # For choosing the port, I am going to pick a closed port and open
            # it, based on the idea that it is guaranteed to not interfere with
            # other processes, however I think picking the port based on any
            # given criteria is as valid.
            if sock.connect_ex((HOST, PORT)) == 0:
                pass # The port is open so go through the loop again.
            else:
                break # The port is closed so break out with this port selected.
    return PORT

def start_server(PORT):
    Popen(
        ["python3", "./server.py", "PORT"], 
        shell=False, 
        stdout=PIPE, 
        stderr=PIPE
        )

def main():
    PORT = find_socket()
    start_server(PORT)
    sys.exit(0)

if __name__ == "__main__":
    main()
