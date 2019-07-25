#!/usr/bin/env python3
"""
	Allan Millar
	testing script
"""
import sys, socket, time, json, logging, pexpect
# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidfunc import find_port, get_ip
from boidfunc import update_profile_self, server_status

def main():
    PORT = find_port()
    IP = get_ip()
    server = pexpect.spawn(
        "python3 ../silla/server.py {} {}".format(PORT, IP)
    )
    server.logfile = sys.stdout.buffer
    update_profile_self(PORT, IP)
    server.expect(pexpect.EOF) # wait for server to finish starting up.
    while True:
        command = input()
        server.sendline(command)
        print (server.before)
        if command == "exit":
            server.close()
            break
    
    sys.exit(0)

if __name__ == "__main__":
    main()