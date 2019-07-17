#!/usr/bin/env python3
"""
	Allan Millar
	testing script
"""
import sys, os, json
from subprocess import Popen, PIPE

# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidload import find_port

def main():
    PORT = str(find_port())
    print (PORT)
    conn_data =  os.path.isfile("../resources/profile.json")
    if conn_data:
        with open("../resources/profile.json", "r+") as file:
            data = json.load(file)
    else:
        with open("../resources/profile.json", "w") as file:
            data = {}
            data["self"] = {}
            data["self"]["port"] = PORT
            #add machine profile information here. The actual profiling 

if __name__ == "__main__":
    main()