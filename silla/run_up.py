#!/usr/bin/env python3
"""
	Allan Millar
	Server initialization program
"""
import sys, os, json, socket
from subprocess import Popen

# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidfunc import find_port

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

def update_profile(PORT, IP):
    conn_data =  os.path.isfile("../resources/profile.json")
    if conn_data:
        # It already exists
        with open("../resources/profile.json", "r") as profile_file:
            data = json.load(profile_file)
        
        data["self"]["port"] = PORT
        data["self"]["ip_addr"] = IP
        
        with open("../resources/profile.json", "w") as profile_file:
            json.dump(data, profile_file, indent=4, sort_keys=True)
    else:
        # It doesn't exist already, should only be reached by source.
        with open("../resources/profile.json", "w") as profile_file:
            data = {"self":{},"parent":{}, "children":{}}
            #cwd = os.getcwd()    If profile.json were to be accidentally deleted
            #if "silla" in cwd:         this would be useful, though I am going to
            #    data["parent"] = {} assume safety.
            data["self"]["port"] = PORT
            data["self"]["ip_addr"] = IP
            json.dump(data, profile_file, indent=4, sort_keys=True)

def main():
    PORT = str(find_port())
    IP = get_ip()
    #Popen(["./server.py", PORT])
    update_profile(PORT, IP)

if __name__ == "__main__":
    main()