#!/usr/bin/env python3
"""
	Allan Millar
	Package sending script
"""
import os
import tarfile
from pathlib import Path
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

def main():
    tar_file =  os.path.isfile("../prf.tar.gz")
    if tar_file:
        os.remove("../prf.tar.gz")
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc/")#, filter=reset)
            tar.add("../resources/")#, filter=reset)
            tar.add("../silla/")#, filter=reset)
    else:
        with tarfile.open("prf.tar.gz", mode="w:gz") as tar:
            tar.add("../boidfunc/")#, filter=reset)
            tar.add("../resources/")#, filter=reset)
            tar.add("../silla/")#, filter=reset)
    
    #Move the tar file up one level.
    p = Path("./prf.tar.gz").absolute()
    parent_dir = p.parents[1]
    p.rename(parent_dir / p.name)
    
    try:
        os.mkdir("../prf/")
    except
    tar = tarfile.open("../prf.tar.gz", "r:gz")
    tar.extractall(path="..")
    tar.close()

if __name__ == "__main__":
    main()


"""
Steps
 - don't name the tar boidload for secrecy
 - tar the three relevant (so far) directories and send to new directory
 - send command to de-tar
 - send command to run start up script
"""