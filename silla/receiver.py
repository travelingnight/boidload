#!/usr/bin/env python3
"""
	Allan Millar
	Package de-tar and client initialization script
"""
import sys, os, tarfile, logging
from subprocess import Popen

def main():
    logging.debug("Entered main method")

    # Tarfile will be sent first so de-tar it.
    tar_file = os.path.isfile("./prf.tar.gz")
    if tar_file: #Tar file exists. Should always be true.
        with tarfile.open("./prf.tar.gz") as tar:
            logging.debug("Attempting extraction of tar file")
            tar.extractall(path="./prf")
    else: #Doesn't exist.
        logging.debug("Tar file not found")
        pass
        # This should ideally never happen, though a robust program should take
        # into account, especially if actually being used. I am currenlty going to
        # ignore this so as to prioritize a simple working prototype.
    
    # Delete the tarfile
    os.remove("./prf.tar.gz")
    logging.debug("tar file deleted.")
    
    # Run the client initilization program. client.py, within silla
    Popen(["python3", "prf/silla/client.py"])
    logging.debug("client.py initiated")

    logging.info("end of program.")
    # This program will then be deleted by client.py
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        filename="receiver.log", 
        filemode="w", 
        format="%(process)d - %(asctime)s -" + 
            "%(funcName)s - %(levelname)s -  %(message)s\n"
    )
    logging.info("starting")
    main()