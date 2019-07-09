"""
    Notes / Temp file
    Allan M.
"""

def mainUserMenu():
    
    with CursesWindow():
        #Initializaing the command line menu
        screen = curses.initscr()
        curses.noecho()
        screen.keypad(1)
        curses.cbreak()
        
        while True:
            userChoice = character(screen)
            screen.clear()
            screen.refresh()
            if userChoice == 0:
                #ssh()
            elif userChoice == 1:
                subprocess.Popen(
                    ["python3", 
                    "/home/allan/boidload/test2.py"]
                    )
            elif userChoice == 2:
                subprocess.Popen(["bash", "./bashTest.sh", str(555)])
            elif userChoice == 3:
                break
            else:
                print ("Something is wrong")
        
        #Shutting down the command line menu
        curses.nocbreak()
        curses.echo()
        screen.keypad(0)
        curses.endwin()


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