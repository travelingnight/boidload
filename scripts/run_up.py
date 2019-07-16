#!/usr/bin/env python3
"""
	Allan Millar
	Server initialization program
"""
import sys, os
from subprocess import run, PIPE

# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidload import find_port, Daemon

class MyDaemon(Daemon):
    def run(self):
        run(
            ["python3", "./server.py", "PORT"], 
            shell=True, 
            stdout=PIPE, 
            stderr=PIPE
            )
        

def main():
    PORT = find_port()
    print (PORT)
    daemon = MyDaemon("/tmp/server.pid")
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print ("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print ("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)

if __name__ == "__main__":
    main()