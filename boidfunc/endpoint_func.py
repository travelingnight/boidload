#!/usr/bin/env python3
"""
	Allan Millar
    Various functions related to sockets, ip's, port's etc.
"""
import sys, random, socket
from contextlib import closing

def find_port():
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

def get_ip():
    #https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    # Where I got this function
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP