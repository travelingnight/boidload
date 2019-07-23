#!/usr/bin/env python3
"""
	Allan Millar
    Various functions related to managing boidload json files
"""

import os, json

def update_profile_self(PORT, IP):
    conn_data =  os.path.isfile("../resources/profile.json")
    if conn_data:
        # It already exists
        with open("../resources/profile.json", "r") as profile_file:
            data = json.load(profile_file)
        
        data["self"]["port"] = PORT
        data["self"]["ip_addr"] = IP
        data["self"]["server_running"] = True
        
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
            data["self"]["server_running"] = True
            json.dump(data, profile_file, indent=4, sort_keys=True)
    return

def server_status():
    """Used to tell if server.py is running
    
    Parameters
    ---------------
    None
    
    Returns
    ----------
    boolean
    
    Raises
    ---------
    """
    conn_data =  os.path.isfile("../resources/profile.json")
    if conn_data:
        # It already exists
        with open("../resources/profile.json", "r") as profile_file:
            data = json.load(profile_file)
            if data["self"]["server_running"] == True:
                return True
            else:
                return False
    else:
        return False