#!/usr/bin/env python3
"""
	Allan Millar
    Remote client script, also serves as remote controller, receiving and 
	processing commands from parent machine.
"""

import sys, socket, time, json, logging

def adjust_profile():
            #Currently doesn't work. Deletes eveything
    try:
        with open("../resources/profile.json", "r") as profile_file:
            data = json.load(profile_file)
        
        data.pop("parent", None)
        data["parent"] = data["self"]
        data.pop("self", None)
        data["self"] = {}
        
        with open("../resources/profile.json", "w") as profile_file:
            json.dump(data, profile_file, indent=4, sort_keys=True)
    except IOError as e:
        pass

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
            logging.info("Received {}.",format(repr(data.decode())))
        
    return
        

def main():
    logging.info("adjusting profile.json to reflect local hierarchy")
    #adjust_profile()
    
    logging.info("fetching connection info for parent")
    with open("../resources/profile.json", "r") as profile_file:
        data = json.load(profile_file)
    PORT = data["self"]["port"]
    IP = data["self"]["ip_addr"]
    
    logging.info("launching client and connecting to parent server")
    launch_client(PORT, IP)
    
    logging.info("end of program")
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        filename="client.log", 
        filemode="w", 
        format="%(asctime)s - %(funcName)s -" + 
            " %(levelname)s -  %(message)s\n"
    )
    logging.info("starting")
    main()