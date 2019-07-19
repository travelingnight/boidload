#!/usr/bin/env python3
"""
	Allan Millar
	Grabs any available connections and stores
	there info in profile in json file.
    
    The Idea is that any machine information will be added to a json file
    called index.json, maybe except for those which have already 
    successfully been integrated into the CapNet, since their information
    will already exist in at least on profile.json.
    
    It is a question though. I imagine personally every machine that is visible to
    a given machine will be indexed, and that those which are already connected
    will simply be marked as such.
    
    Perhaps there could be five categories.
     - Integrated: Already captured and connected to the CapNet.
     - Vulnerable: Not integrated but ready to be captured.
     - Secure: Not integrated and currently not capturable.
     - Dangerous: Not integrated and risky to attack or interact with (maybe).
     - Unknown: Visible, but has not been profiled.
    This is just my idea for when it is eventually fully functional.
    
    For now this will be hard coded to add three computers, two VM's and 
    one fake one for simulating a secure computer.
"""
import os, json

def main():
    


if __name__ == "__main__":
    main()