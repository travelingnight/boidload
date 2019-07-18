#!/usr/bin/env python3
"""
	Allan Millar
	Package sending script
"""
import os, tarfile, time
from pathlib import Path
from subprocess import Popen, PIPE
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
    proc = Popen(
        ["ssh", "-T", "aiaasboi@134.129.92.168", "-p", "2097"],
        stdin=PIPE,
        stdout=PIPE,
        universal_newlines=True
        )
    proc.stdin.write("aiaasboi\n")
    return proc

def deliver_package(proc):
    proc2 = Popen(
        ["netcat", "-l", "4444", ">", "prf.tar.gz"], 
        stdin=proc.stdout, 
        stdout=PIPE
        )
    proc_send_reciever = Popen(
        ["scp", "-P", "4444", "../prf.tar.gz", "aiaasboi@134.129.92.168"]
        )
    time.sleep(3)
    proc3 = Popen(
        ["netcat", "-l", "4444", ">", "receiver.py"], 
        stdin=proc2.stdout, 
        stdout=PIPE
        )
    proc_send_reciever = Popen(
        ["scp", "-P", "4444", "./receiver.py", "aiaasboi@134.129.92.168"]
        )
    return proc3

def initiate(proc):
    proc2 = Popen(
        ["python3", "reciever.py"], 
        stdin=proc.stdout, 
        )

def disconnect(proc):
    proc.stdin.write("exit\n")

def main():
    print ("construct_package")
    construct_package()
    print ("ssh_connect")
    proc = ssh_connect()
    print ("deliver_package")
    #proc = deliver_package(proc)
    #time.sleep(3)
    print ("initiate")
    #initiate(proc)
    print ("disconnect")
    disconnect(proc)

if __name__ == "__main__":
    main()


"""
Steps
 - don't name the tar boidload for secrecy
 - tar the three relevant (so far) directories and send to new directory
 - send receiver.py and execute
"""