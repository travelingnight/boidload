#!/usr/bin/env python3
"""
	Allan Millar
	Package receiving and client initialization script
"""
import os
import tarfile
from pathlib import Path
from subprocess import Popen

def main():
    construct_package()
    proc = ssh_connect()
    deliver_startup(proc)

if __name__ == "__main__":
    main()