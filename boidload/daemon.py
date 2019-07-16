"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal

"""
An Ideal daemon process should satisfy the following conditions
according to PEP 3143.

-Close all open file descriptors.
-Change current working directory. (chdir)
-Reset the file access creation mask. (umask)
-Run in the background.
-Disassociate from process group.
-Ignore terminal I/O signals.
-Disassociate from control terminal. (first fork)
-Don’t reacquire a control terminal. (second fork)
-Correctly handle the following circumstances:
    -Started by System V init process.
    -Daemon termination by SIGTERM signal.
    -Children generate SIGCLD signal.

I don't think mine is technically a daemon, as I want any given computer
to be able to communicate with it.
"""

class Daemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile): self.pidfile = pidfile
    
    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        
        try:
            pid = os.fork()
            """ os.fork() creates a child process, so immediately following there
            are actually two processes running. They are running the exact
            same code, even in terms of all their variables, except for the value
            returned from os.fork() itself.
            
            The value returned to the child is 0
            The value returned to the parent is the child's process ID, or pid
            
            If we don't want the parent process we can have both check
            themselves and have the not-parent terminate.
            """
            if pid > 0:
                # exit first parent
                sys.exit(0)
        #os.fork() returns an OSError on failure.
        except OSError as err: 
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)
    
        # decouple from parent environment
        """Explanation I found for changing the directory.
        
        'Why change working directory to the root directory? Well, it allows 
        the system administrator to mount and unmount directories without
        your daemon getting in the way. If you have seen the error 
        messages such as
        
        umount: /usr: device is busy
        
        you will be familiar with the problem. The root directory may not 
        always be the best choice - sometimes it is more appropriate to 
        change to the directory containing all your daemons data files.
        Then if the sysadmin tries to unmount that directory, the device 
        busy message may be a good reminder that there exists a process 
        which still needs that data.'"""
        os.chdir('/')
        
        """Fantastic answer regarding why we use setsid to change the newly
        forked processes group ID to itself.
        
        'Calling setsid is usually one of the steps a process goes through 
        when becoming a so called daemon process. (We are talking about 
        Linux/Unix OS)
        
        With setsid the association with the controlling terminal breaks. 
        This means that the process will be NOT affected by a logout.
        
        There are other way how to survive a logout, but the purpose of 
        this 'daemonizing' process is to create a background process as 
        independent from the outside world as possible.
        
        That's why all inherited descriptors are closed; cwd is set to an 
        appropriate directory, often the root directory; and the process 
        leaves the session it was started from.
        
        A double fork approach is generally recommended. At each fork 
        the parent exits and the child continues. Actually nothing changes 
        except the PID, but that's exactly what is needed here.
        
        First fork before the setsid makes sure the process is not a process 
        group leader. That is required for a succesfull setsid.
        
        The second fork after the setsid makes sure that a new association 
        with a controlling terminal won't be started merely by opening a 
        terminal device."""
        os.setsid()
        
        """umask sets the umask (user file-creation mode mask). The umask 
        determines the permissions and denials for any newly-created files
        and directories. Specifically I am referring to the rwxrwxrwx values.
        
        If I'm not mistaken, we set it to zero because we don't want anything
        interacting with the process while it runs."""
        os.umask(0) 
    
        # do second fork, for reasons discussed above.
        try: 
            pid = os.fork() 
            if pid > 0:

                # exit from second parent
                sys.exit(0) 
        except OSError as err: 
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1) 
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'w')
        se = open(os.devnull, 'w')
         
        #os.dup2(si.fileno(), sys.stdin.fileno())
        #os.dup2(so.fileno(), sys.stdout.fileno())
        #os.dup2(se.fileno(), sys.stderr.fileno())
        
        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        print (pid)
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
        
    def delpid(self):
        print ("Here we go")
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""
        
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile,'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if pid:
            message = "Start: pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if not pid:
            message = "Stop: pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print (str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.
        
        It will be called after the process has been daemonized by 
        start() or restart()."""
