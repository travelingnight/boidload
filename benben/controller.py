#!/usr/bin/env python
"""
	Allan Millar
	Main control program
"""

import sys, curses, subprocess


class CursesWindow(object): #Context Wrapper
    def __enter__(self):
        curses.initscr()

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            #return False #Uncomment to pass exception through
        curses.endwin()
        return True


def menuHandling(screen, menuNum):
    
    menuNameList=[
        "ezhack Controller Main Menu\n",
        "CapNet Management Menu\n", 
        "Activation Menu\n", 
        "Deactivation Menu\n", 
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
        "Back"]
    ]
    
    attributes = {} #Empty dictionary
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
            menuNameList[menuNum], 
            curses.A_UNDERLINE
        )
        for i in range(len(menuOptionCollection[menuNum])):
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            screen.addstr("{0}. ".format(i+1))
            screen.addstr(menuOptionCollection[menuNum][i] + '\n', attr)
        c = screen.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN:
            if option < len(menuOptionCollection[menuNum])-1:
                option += 1
                
    return option

def mainMenu(screen, menuNum):
    while True:
        userChoice = menuHandling(screen, menuNum)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            managementMenu(screen, 1)
        elif userChoice == 1:
            activationMenu(screen, 2)
        elif userChoice == 2:
            deactivationMenu(screen, 3)
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return True

def closingPrint():
    print("All processes shutting down.")

def managementMenu(screen, menuNum):
    while True:
        userChoice = menuHandling(screen, menuNum)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            profileCapNet()
        elif userChoice == 1:
            expandCapNet()
        elif userChoice == 2:
            guidedExpandCapNet()
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return True

def profileCapNet():
    print ("\nProfile\n")
    return

def expandCapNet():
    print ("\nExpand\n")
    return

def guidedExpandCapNet():
    print ("\nGuided Expand\n")
    return


def activationMenu(screen, menuNum):
    while True:
        userChoice = menuHandling(screen, menuNum)
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
    return True

def deactivationMenu(screen, menuNum):
    while True:
        userChoice = menuHandling(screen, menuNum)
        screen.clear()
        screen.refresh()
        if userChoice == 0:
            pauseCapNet()
        elif userChoice == 1:
            extractCapNet()
        elif userChoice == 2:
            offloadTaskload()
        elif userChoice == 3:
            break
        else:
            print ("Something is wrong")
    return True

def pauseCapNet():
    print ("\nPause\n")
    return

def extractCapNet():
    print ("\nExtract\n")
    return

def offloadTaskload():
    print ("\nOffload\n")
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