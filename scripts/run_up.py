#!/usr/bin/env python3
"""
	Allan Millar
	Program solely made to find an unused port and return it's number.
"""

def start_server(PORT):
    run(
        ["python3", "./server.py", "PORT"], 
        shell=False, 
        stdout=PIPE, 
        stderr=PIPE
        )

def main():
    PORT = boidload.find_port()
    print (PORT)
    start_server(PORT)
    sys.exit(0)

if __name__ == "__main__":
    import sys, random, socket
    from contextlib import closing
    from subprocess import run, PIPE
    
    # Adding in a path to import boidload, which is one directory up.
    sys.path.insert(0, "../")
    import boidload
    main()
