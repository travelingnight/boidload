#!/usr/bin/env python
"""
	Allan Millar
	Main control program
"""

import sys, curses, pexpect
# Adding in a path to import boidload, which is one directory up.
sys.path.insert(0, "../")
#import boidload
from boidfunc import find_port, get_ip
from boidfunc import update_profile_self, server_status, deactivate_server


# This global value could definitely be considered a work around, as I am
# doing it because it's the easiest option and curses is the most confusing
# part of all of this code.
global_server = None

class CursesWindow(object): #Context Wrapper
    def __enter__(self):
        curses.initscr()

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            #return False #Uncomment to pass exception through
        curses.endwin()
        return True


def menuHandling(screen, menu_num):
    
    menuNameList=[
        "ezhack Controller Main Menu\n",
        "CapNet Management Menu\n", 
        "Activation Menu\n", 
        "Deactivation Menu\n",
        "Expansion Menu"
    ]

    menuOptionCollection=[
        ["CapNet Management Menu", 
        "Activation Menu", 
        "Deactivation Menu", 
        "Full System Shutdown"
        ], 
        ["Profile CapNet (Not Implemented)",
        "Expand CapNet (Not Implemented)",
        "Guided Expansion (Not Implemented)",
        "Back"],
        ["ActOp1", "ActOp2", "ActOp3", "Back"],
        ["Pause All Activity (Not Implemented)",
        "Extract (Not Implemented)",
        "Offload (Not Implemented)",
        "Back"],
        ["Press enter to stop expanding"]
    ]
    
    attributes = {}
    #Populating attributes with color combos of font and 
    # background, like highlighting.
    """ initialize color pallet """
    curses.start_color()
    if not curses.has_colors():
        raise RuntimeError("Sorry. Terminal does not support colors")
    
    curses.init_pair(
        1, 
        curses.COLOR_WHITE, 
        curses.COLOR_BLACK
    )
    attributes['normal'] = curses.color_pair(1)
    
    curses.init_pair(
        2, 
        curses.COLOR_BLACK, 
        curses.COLOR_WHITE
    )
    attributes['highlighted'] = curses.color_pair(2)
    
    c = 0 #Last character read
    option = 0 #The current option that is marked
    while c != 10: #10 is \n  in ascii
        screen.erase()
        screen.addstr(
            menuNameList[menu_num], 
            curses.A_UNDERLINE
        )
        for i in range(len(menuOptionCollection[menu_num])):
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            screen.addstr("{0}. ".format(i+1))
            screen.addstr(menuOptionCollection[menu_num][i] + '\n', attr)
        c = screen.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN:
            if option < len(menuOptionCollection[menu_num])-1:
                option += 1
                
    return option

def mainMenu(screen, menu_num):
    while True:
        userChoice = menuHandling(screen, menu_num)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            managementMenu(screen, 1)
        elif userChoice == 1:
            activationMenu(screen, 2)
        elif userChoice == 2:
            deactivationMenu(screen, 3)
        elif userChoice == 3:
            extract()
            break
        else:
            print ("Something is wrong")
    return True

def closingPrint():
    print("All processes shutting down.")

def managementMenu(screen, menu_num):
    while True:
        userChoice = menuHandling(screen, menu_num)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            profileCapNet()
        elif userChoice == 1:
            expandCapNet(screen, 4)
        elif userChoice == 2:
            guidedExpandCapNet()
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return

def profileCapNet():
    pass
    # If profile.json exists and server_running = True,
    #   send command to profile and profile local machine.
    # If profile.json exists and server_running = False,
    #   profile local machine only
    # If profile.json doesn't exist,
    #   create profile.json and profile local machine.
    return

def expandCapNet(screen, menu_num):
    """Establish server and/or send command to expand."""
    if not server_status():
        # If the server isn't already running, start it up first.
        PORT = find_port()
        IP = get_ip()
        server = pexpect.spawn(
            "python3 ../silla/server.py {} {}".format(PORT, IP)
        )
        server.sendline("")
        global global_server
        global_server = server
        update_profile_self(PORT, IP)
        #server.expect(pexpect.EOF)
    
    # Send the command to the server
    global_server.sendline("expand")
    
    while True:
        # This doesn't actually do anything since expansion is currently
        # hard-coded and stops on it's own.
        userChoice = menuHandling(screen, menu_num)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            server.sendline("halt")
            break
        else:
            print ("Something is wrong")
    return

def guidedExpandCapNet():
    pass
    # Go to sub-menu where user can enter values for things like individual
    # machine, ip group, category, etc.
    return


def activationMenu(screen, menu_num):
    while True:
        userChoice = menuHandling(screen, menu_num)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            pass
        elif userChoice == 1:
            pass
        elif userChoice == 2:
            pass
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return

def deactivationMenu(screen, menu_num):
    while True:
        userChoice = menuHandling(screen, menu_num)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            pass
        elif userChoice == 1:
            extract()
        elif userChoice == 2:
            pass
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return

def extract():
    """Establish server and/or send command to expand."""
    if not server_status():
        # No server, so nothing to extract
        return
    
    # Send the command to the server
    global_server.sendline("extract")
    global_server.close()
    deactivate_server()
    return

def main():
    # Profile machine and add to profile.json
    while True:
        with CursesWindow():
            #Initializaing the command line menu
            screen = curses.initscr()
            curses.noecho()
            screen.keypad(1)
            curses.cbreak()
            if mainMenu(screen, 0):
                break
            
             #Shutting down the command line menu
            curses.nocbreak()
            curses.echo()
            screen.keypad(0)
            curses.endwin()
    
    closingPrint()
    sys.exit(0)

if __name__ == "__main__":
    main()