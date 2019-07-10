#!/usr/bin/env python3
"""
    Allan Millar
    Server
    Massive credit to
    https://github.com/eliben/python3-samples/blob/3a533b22c97c54de22d9cf950a9a3247739eaddc/async/selectors-async-tcp-server.py
    From which I constructed this server architecture/program.
"""
import sys, socket, selectors, logging, time, argparse

keep_running = True

class SelectorServer:
    def __init__(self, host, port):
        # Create the main socket that accepts incoming connections
        # and start listening. The socket is nonblocking.
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(20)
        self.main_socket.setblocking(False)
        
        # Initialize a default selector that will handle the events.
        # Register main_socket for monitoring, monitor READ events 
        # and READ events, and the handler method is passed in data
        # so we can fetch it in servee_forever. on_accept is the handler
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
        try:
            data = conn.recv(1024)
            if (data.decode() == "Close connection"):
                self.close_connection(conn)
            elif (data.decode() == "Shut off server"):
                peername = conn.getpeername()
                logging.info("Data received from " + 
                    "{}: {!r}".format(peername, data)
                    )
                data = "Full shutdown"
                conn.send(data.encode())
                self.shutdown()
            else:
                peername = conn.getpeername()
                logging.info("Data received from " + 
                    "{}: {!r}".format(peername, data)
                    )
                # Assume for simplicity that send won't block, (I don't know)
                conn.send(data)
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
            #logging.debug("Reached end of for loop.")
            # This part happens roughly every second
            current_time = time.time()
            if current_time - last_report_time > 1:
                #logging.debug("Inside of if statement")
                logging.info("Running report ...")
                if (len(self.current_peers) > 0):
                    logging.info("Num active peers = {0}".format(
                        len(self.current_peers)))
                last_report_time = current_time
        logging.debug("Flag successfully changed, exiting serve_forever")

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("port", 
        help = "use the provided number as the port for the server", 
        type = int
        )
    args = parser.parse_args()
    print (args)
    
    logging.debug("Entered main method")
    HOST = "localhost" #Simplified for development
    PORT = args.port
    
    server = SelectorServer(host = HOST, port = PORT)
    server.serve_forever()
    
    logging.info("Program closing")
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        filename="app.log", 
        filemode="w", 
        format="%(process)d - %(asctime)s -" + 
            "%(funcName)s - %(levelname)s -  %(message)s\n"
        )
    logging.info("starting")
    main()