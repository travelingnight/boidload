#!/usr/bin/env python3
"""
	Allan Millar
	Server initialization program
"""

def start_server(PORT):
    run(
        ["python3", "./server.py", "PORT"], 
        shell=True, 
        stdout=PIPE, 
        stderr=PIPE
        )

def main():
    PORT = find_port()
    print (PORT)
    daemonize()
    start_server(PORT)
    sys.exit(0)

if __name__ == "__main__":
    import sys, random, socket
    from subprocess import run, PIPE
    
    # Adding in a path to import boidload, which is one directory up.
    sys.path.insert(0, "../")
    #import boidload
    from boidload import find_port, daemonize
    main()
