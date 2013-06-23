'''
Created on 19 May 2013

Simple HTTP server to accept images and sensor data to assemble data sets

@author: dsnowdon
'''

import sys
import os
import urlparse
import cgi
import BaseHTTPServer

DATA_DIR=None
PREFIX=None
INDEX = 0

class CollectorRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        global DATA_DIR
        global PREFIX
        global INDEX
        print "got POST\n"
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        print postvars['sensordata']
        filedata = postvars['fileupload']
        basename = "{prefix}-{index:04d}".format(prefix=PREFIX, index=INDEX)
        if filedata:
            filename = basename + ".jpg"
            path = os.path.join(DATA_DIR, filename)
            with open(path, "wb") as out:
                out.write(''.join(filedata))
            
        sensordata = postvars['sensordata']
        if sensordata:
            print "Sensordata: {}\n".format(sensordata)
            json_filename = basename + ".json"
            path = os.path.join(DATA_DIR, json_filename)
            with open(path, "w") as out:
                out.write("{}\n".format(sensordata))

        INDEX = INDEX + 1
        
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()


class CollectorHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, serverAddress, requestClass):
        # HTTPServer is not a new style class
        BaseHTTPServer.HTTPServer.__init__(self, serverAddress, requestClass)

def make_server(port):
    server_address = ('', port)
    httpd = CollectorHTTPServer(server_address, CollectorRequestHandler)
    return httpd

def start_server(httpd):
    httpd.serve_forever()

def stop_server(httpd):
    httpd.shutdown()

def main(argv=None):
    global DATA_DIR
    global PREFIX
    DATA_DIR = argv[1]
    PREFIX = argv[2]
    print "dir = {dir}, prefix = {prefix}".format(dir=DATA_DIR, prefix = PREFIX)
    
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except OSError:
            print("Failed to create dir: {}".format(DATA_DIR))
            return 1
    
    httpd = make_server(8080)
    start_server(httpd)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))