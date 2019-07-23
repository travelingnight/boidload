#!/usr/bin/env python3
"""
	Allan Millar
	testing script
"""
import sys, os
from pexpect import pxssh
import getpass

def main():
    pass


if __name__ == "__main__":
    main()
"""
import os
import json

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
(path)]
    else:
        d['type'] = "file"
    return d
"""
"""
cwd = os.getcwd()
print (cwd)
if "benben" in cwd:
    print("Source")
else:
    print("Captured")
"""