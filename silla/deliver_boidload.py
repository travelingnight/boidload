#!/usr/bin/env python3
"""
	Allan Millar
	Package sending and initiating script
"""
import os, tarfile, time, pexpect
from pathlib import Path
"""
This method may be necessary to some degree if there are issues with
permissions, but for nwo it's not necessary.
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
    """Grabbing the files we want to send and adding them to a compressed tar
    file. The if simply checks if the tar exists and needs to be replaced."""
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
    """
    Spawns a pexpect object which in this case is the connection to the VM.
    The object ssh's into the VM, waits for the password prompt, and passes
    the password.
    
    This will have to dynamically load passwords and api's and stuff, and
    assuming there ever is automated hacking there may be some redundancy.
    """
    ssh = pexpect.spawn("ssh -T aiaasboi@134.129.92.168 -p 2097")
    ssh.expect("password:", timeout=120)
    ssh.sendline("aiaasboi")
    return ssh

def deliver_package(ssh):
    """
    Using the same object tell the VM to expect a file.
    Start another process on the local machine to send the tar of boidload.
    Tell the VM to expect another file, this time receiver.py.
    Using the same process that sent the tar, send the script.
    
    Again the machine info will eventually need to be written dynamically.
    """
    ssh.sendline("netcat -l 4444 > prf.tar.gz")
    time.sleep(1)
    scp = pexpect.spawn("scp -P 4444 ../prf.tar.gz aiaasboi@134.129.92.168")
    time.sleep(1)
    ssh.sendline("netcat -l 4444 > receiver.py")
    time.sleep(1)
    scp.sendline("scp -P 4444 ./receiver.py aiaasboi@134.129.92.168")
    return ssh

def initiate(ssh):
    """Start receiver.py which should initiate another connection from within
    boidload."""
    ssh.sendline("python3 reciever.py")

def disconnect(ssh):
    ssh.sendline("exit")

def main():
    print ("construct_package")
    construct_package()
    print ("ssh_connect")
    ssh = ssh_connect()
    print ("deliver_package")
    ssh = deliver_package(ssh)
    print ("initiate")
    initiate(ssh)
    print ("disconnect")
    disconnect(ssh)

if __name__ == "__main__":
    main()


"""
Steps
 - don't name the tar boidload for secrecy
 - tar the three relevant (so far) directories and send to new directory
 - send receiver.py and execute
"""