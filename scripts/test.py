#!/usr/bin/env python3
"""
	Allan Millar
	Server initialization program
"""
import sys, os
from subprocess import Popen, PIPE

# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidload import find_port

def main():
    PORT = str(find_port())
    print (PORT)
    Popen(["./server.py", PORT])

if __name__ == "__main__":
    main()