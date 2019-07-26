#!/usr/bin/env python3
"""
	Allan Millar
	testing script
"""
import sys, time, pexpect, os
# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidfunc import find_port, get_ip
def main():
    PORT = find_port()
    IP = get_ip()
    print (PORT)
    print (IP)
    print (os.getcwd())
    print ("python3 ../silla/server.py {} \"{}\"".format(PORT, IP))
    server = pexpect.spawn(
        "python3 ../silla/server.py {} \"{}\"".format(PORT, IP)
    )
    time.sleep(5)
    server.sendline("expand")
    time.sleep(5)
    server.close()
    sys.exit(0)

if __name__ == "__main__":
    main()