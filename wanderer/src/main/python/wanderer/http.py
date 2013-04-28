'''
Created on 12 Apr 2013

@author: dsnowdon
'''

import os
import posixpath
import mimetypes
import shutil
import BaseHTTPServer

from naoutil.jsonobj import to_json_file
import wanderer

def make_server(env, port):
    server_address = ('', port)
    httpd = NaoHTTPServer(env, server_address, NaoRequestHandler)
    return httpd

def start_server(httpd):
    httpd.serve_forever()

def stop_server(httpd):
    httpd.shutdown()


class NaoHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, env_, serverAddress, requestClass):
        # HTTPServer is not a new style class
        BaseHTTPServer.HTTPServer.__init__(self, serverAddress, requestClass)
        self.env = env_
    
    def get_mapper(self):
        return wanderer.get_mapper_instance(self.env)
    
    def get_data(self, key):
        return self.env.memory.getData(key)
    
    def localized_text(self, basename, propertyName):
        return self.env.localized_text(basename, propertyName)


class NaoRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def get_env(self):
        return self.server.env

    def do_HEAD(self):
        self.server.env.log("HEAD: "+self.path)
        self.handle_request(False)

    def do_GET(self):
        self.server.env.log("GET: "+self.path)
        self.handle_request(True)

    def handle_request(self, send_content):
        self.server.env.log("REQUEST: "+self.path)
        # list of possible actions, need to have longest paths first for matching to work
        responses = [
                     ('/actions/done' , self.do_actions_done),
                     ('/actions/planned' , self.do_actions_planned),
                     ('/actions/current' , self.do_actions_current),
                     ('/action' , ['done', 'planned', 'current']),
                     ('/raw/sensed' , self.do_raw_sensed),
                     ('/raw/path' , self.do_raw_path),
                     ('/raw' , ['sensed', 'path']),
                     ('/map/json' , self.do_map_json),
                     ('/map/image' , self.do_map_image),
                     ('/map' , ['json', 'image']),
                     ]
        
        rq = self.path.lower()
        requestCompleted = False
        for prefix, action in responses:
            if rq.startswith(prefix):
                # is action to take a function or literal
                if hasattr(action, '__call__'):
                    params = rq[len(prefix):]
                    action(send_content, params)
                else:
                    self.json_response(send_content, action)
                requestCompleted = True
                break
        if not requestCompleted:
            if self.path == '/':
                self.do_index(send_content, rq)
            else:
                self.do_static_file(send_content, rq)

    def json_header(self, size=None):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        if size:
            self.send_header("Content-Length", size)
        self.end_headers()

    def json_response(self, send_content, obj):
        self.json_header()
        if send_content:
            to_json_file(obj, self.wfile)

    def text_response(self, send_content, msg):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=UTF-8")
        self.send_header("Content-Length", len(msg))
        self.end_headers()
        if send_content:
            self.wfile.write(msg)

    def send_404(self, path):
        env = self.get_env()
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(env.localized_text("defaults", "error.web.404"))

    def do_index(self, send_content, params):
        self.do_static_file(send_content, "index.html")

    # serve static files located in /resources/web
    def do_static_file(self, send_content, path):
        if path.startswith("/"):
            path = path[1:]
        file_path = os.path.join(self.server.env.resources_dir(), wanderer.STATIC_WEB_DIR, path)
        self.server.env.log("REQUEST: File "+path+" mapped to "+file_path)
        (content_type, encoding) = mimetypes.guess_type(file_path)
        self.copy_file_to_output(send_content, file_path, content_type)

    def copy_file_to_output(self, send_content, src, content_type, buffer_size=1024):
        if content_type.startswith('text/'):
            mode = 'r'
            content_type = content_type + '; charset=UTF-8'
        else:
            mode = 'rb'
        try:
            try:
                fp = open(src, mode)
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.send_header("Content-Length", os.path.getsize(src))
                self.end_headers()
                if send_content:
                    while 1:
                        copy_buffer = fp.read(buffer_size)
                        if copy_buffer:
                            self.wfile.write(copy_buffer)
                        else:
                            break
            finally:
                fp.close()
        except IOError:
            self.server.env.log("REQUEST: File "+src+" not found")
            self.send_404(src)

    def do_actions_done(self, send_content, params):
        obj = wanderer.load_completed_actions(self.get_env())
        self.json_response(send_content, obj)
    
    def do_actions_current(self, send_content, params):
        obj = wanderer.get_current_action(self.get_env())
        self.json_response(send_content, obj)
    
    def do_actions_planned(self, send_content, params):
        obj = wanderer.load_plan(self.get_env())
        self.json_response(send_content, obj)
    
    def do_raw_sensed(self, send_content, params):
        mapper = self.server.get_mapper()
        raw = mapper.get_sensor_data()
        self.json_header()
        if send_content:
            mapper.write_sensor_data_to_file(self.wfile)

    def do_raw_path(self, send_content, params):
        obj = wanderer.get_path(self.get_env())
        self.json_response(send_content, obj)
    
    def do_map_json(self, send_content, params):
        currentMap = self.server.get_mapper().get_map()
        if currentMap:
            self.json_response(send_content, currentMap)
        else:
            self.text_response(send_content, self.server.localized_text("defaults", "error.unavailable.map.json"))
    
    def do_map_image(self, send_content, params):
        self.text_response(send_content, self.server.localized_text("defaults", "error.notImplemented.map.image"))
        
