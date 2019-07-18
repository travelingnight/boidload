#!/usr/bin/env python3
"""
	Allan Millar
	Server initialization program
"""
import sys, os
from subprocess import Popen

# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidfunc import find_port

def update_port(PORT):
    conn_data =  os.path.isfile("../resources/profile.json")
    if conn_data: # It already exists
        with open("../resources/profile.json", "r+") as file:
            data = json.load(file)
            # I am going to assume that the json has already been adjusted to 
            # reflect it now being the new machine, so what was self is now in
            # parent and so on.
            data["self"]["port"] = PORT
            
    else: # It doesn't exist already, should only be reached by source.
        with open("../resources/profile.json", "w") as file:
            data = {}
            #cwd = os.getcwd()    If profile.json were to be accidentally deleted
            #if "silla" in cwd:         this would be useful, though I am going to
            #    data["parent"] = {} assume safety.
            data["self"] = {}
            data["self"]["port"] = PORT

def main():
    PORT = str(find_port())
    print (PORT)
    Popen(["./server.py", PORT])
    update_port(PORT)

if __name__ == "__main__":
    main()