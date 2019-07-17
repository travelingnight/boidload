#!/usr/bin/env python3
"""
	Allan Millar
	Package sending script
"""
import os
import tarfile
from pathlib import Path
from subprocess import Popen
"""
def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    return tarinfo
"""
"""
We only want to send what is necessary for the computer to do what
we want, so we package only the relevant directories/files. Sending
more may make the system easier to defend against or analyze.
"""
def construct_package():
    tar_file =  os.path.isfile("../prf.tar.gz")
    if tar_file:
        os.remove("../prf.tar.gz")
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc")#, filter=reset)
            tar.add("../resources")#, filter=reset)
            tar.add("../silla")#, filter=reset)
    else:
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc")#, filter=reset)
            tar.add("../resources")#, filter=reset)
            tar.add("../silla")#, filter=reset)
    
    #Move the tar file up one level.
    p = Path("./prf.tar.gz").absolute()
    parent_dir = p.parents[1]
    p.rename(parent_dir / p.name)

def ssh_connect():
    proc = subprocess.Popen(
        ["ssh", "aiaasboi@134.129.92.168", "-p", "2097"],
        stdout=subprocess.PIPE
        )
    proc2 = subprocess.Popen(
        "aiaasboi", 
        stdin=p1.stdout, 
        stdout=subprocess.PIPE
        )
    return proc2

def deliver_startup():

def main():
    construct_package()
    proc = ssh_connect()
    deliver_startup(proc)

if __name__ == "__main__":
    main()


"""
Steps
 - don't name the tar boidload for secrecy
 - tar the three relevant (so far) directories and send to new directory
 - send command to de-tar
 - send command to run start up script
"""

"""
sshBook={} #The dictionary every computer will have storing
                     # the stuff necessary to open all of it's connections
                     # with both the 
def ssh():
    subprocess.Popen(
        ["ssh", "aiaasboi@134.129.92.168", "-p", "2097"], 
        shell=False, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        )
"""