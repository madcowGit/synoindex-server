#-*- coding: utf-8 -*-
import sys
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Basic class to handle HTTP requests
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/synoindex" in self.path:
            # respond to pass arguments to synindex
            query = urlparse(self.path).query
            query_components = parse_qs(query)

            if "args" in query_components:
                args = query_components["args"]
                if len(args) == 1:
                    msg = 'Synoindex NOT Support [%s] argument, but response OK to clients!' % args[0]
                elif len(args) >= 2:
                    msg = indexing(args)
            else:
                msg = 'Synoindex response OK to clients!'

            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg.encode())
        elif "/shutdown" in self.path:
            # shut down server
            self.send_response(200,'shutting down')
            msg = 'Shutting down server'
            self.end_headers()
            self.wfile.write(msg.encode())
            self.server.running = False
        else:
            # if all else fails
            self.send_response(404)
            self.end_headers()

        return

# function that calls synoindex on diskstation
def indexing(arg):
    msg = 'Synoindex %s %s' % (str(arg[0]), str(arg[1]))
    pname = '/usr/syno/bin/synoindex'
    if os.path.isfile(pname):
        try:
            cmd = [pname, arg[0], arg[1].encode('utf-8')]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
        except Exception as e:
            msg = 'Exception:%s' % e
    else:
        msg = 'Synoindex is not exist'
    return msg


# class to allow nice starting/stopping of httpserver
class MainServer:
    def __init__(self, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):        
        server_address = (sys.argv[1],int(sys.argv[2]))
        self._server = server_class(server_address, handler_class)
        self._thread = threading.Thread(target=self.run)
        self._thread.deamon = True
        print('Starting httpd...') 

    def run(self):
        self._server.running = True
        while self._server.running:
            self._server.handle_request()

    def start(self):
        self._thread.start()

    def shut_down(self):
        self._thread.close()


# running the server
if __name__ == "__main__":
    try:
        # create & run server
        m = MainServer()
        m.start()
    except KeyboardInterrupt:
        print('Stopping httpd...')
