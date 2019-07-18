#!/usr/bin/env python3
"""
	Allan Millar
	Package de-tar and client initialization script
"""
import os, tarfile
from subprocess import Popen

def main():
     # Tarfile will be sent first so de-tar it.
     tar_file = os.path.isfile("./prf.tar.gz")
     if tar_file: #Tar file exists. Should always be true.
        with tarfile.open("./prf.tar.gz") as tar:
            tar.extractall()
            # May need to worry about permissions
            # Will probably need to worry about directory structure
     else: #Doesn't exist.
        pass
        # This should ideally never happen, though a robust program should take
        # into account, especially if actually being used. I am currenlty going to
        # ignore this so as to prioritize a simple working prototype.
     
     # Delete the tarfile
     os.remove("./prf.tar.gz")
     
     # Maybe: restructure the files if they aren't extracted correctly.
     
     # Run the client initilization program. client.py, within silla
     subprocess.Popen(["python3", "prf/silla/client.py"])
     
     # This program will then be deleted by client.py

if __name__ == "__main__":
    main()