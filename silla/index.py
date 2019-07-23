#!/usr/bin/env python3
"""
	Allan Millar
	Grabs any available connections and stores
	there info in profile in json file.
    
    The Idea is that any machine information will be added to a json file
    called index.json, maybe except for those which have already 
    successfully been integrated into the CapNet, since their information
    will already exist in at least on profile.json.
    
    It is a question though. I imagine personally every machine that is visible to
    a given machine will be indexed, and that those which are already connected
    will simply be marked as such.
    
    Perhaps there could be five categories.
     - Integrated: Already captured and connected to the CapNet.
     - Vulnerable: Not integrated but ready to be captured.
     - Secure: Not integrated and currently not capturable.
     - Dangerous: Not integrated and risky to attack or interact with (maybe).
     - Unknown: Visible, but has not been profiled.
    This is just my idea for when it is eventually fully functional.
    
    For now this will be hard coded to add four computers, two VM's and 
    two fake ones for simulating other scenarios.
    
    The eventual input would likely be the output of whatever scans the networks
    and profiles the machines found based on whatever arbitrary criteria.
"""
import os, json

def main():
    index_file =  os.path.isfile("../resources/index.json")
    if index_file: # It already exists
        os.remove("../resources/index.json")
    
    data = {
        "integrated":{}, 
        "vulnerable":{}, 
        "secure":{}, 
        "dangerous":{}, 
        "unknown":{}
    }
    data["vulnerable"]["00:0c:29:89:3e:34"] = {
        "username": "aiaasboi",
        "ip_addr": "134.129.92.168",
        "port": "2097",
        "password": "aiaasboi"
    }
    
    data["vulnerable"]["00:0c:29:f5:f4:1a"] = {
        "username": "aiaasboi",
        "ip_addr": "134.129.92.149",
        "port": "22",
        "password": "aiaasboi2"
    }
    
    data["vulnerable"]["00:0c:29:17:18:f1"] = {
        "username": "aiaasboi",
        "ip_addr": "134.129.92.292",
        "port": "2000",
        "password": "aiaasboi"
    }
    data["vulnerable"]["00:0c:29:d4:87:22"] = {
        "username": "aiaasboi",
        "ip_addr": "134.129.92.324",
        "port": "3454",
        "password": "aiaasboi"
    }
    data["secure"]["00:0c:29:d4:87:22"] = {
        "username": "aiaasboi",
        "ip_addr": "134.129.92.324",
        "port": "3454",
        "password": "aiaasboi"
    }

    with open("../resources/index.json", "w") as file:
        json.dump(data, file)

if __name__ == "__main__":
    main()