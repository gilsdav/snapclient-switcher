#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import subprocess
import os
import atexit

name = 'snapclient'
daemon = '/usr/bin/' + name

default_snap_port = '1704'
default_snap_server = '127.0.0.1'

class S(BaseHTTPRequestHandler):

    pro = None
    snap_server = default_snap_server
    snap_port = default_snap_port

    @staticmethod
    def stop_previous_instance():
        if not (S.pro is None):
            S.pro.kill()
            pid = subprocess.check_output('pidof snapclient', shell=True).strip()
            subprocess.call('kill ' + pid, shell=True)
    
    @staticmethod
    def start_new_instance():
        print ('new snapclient')
        print (S.snap_server)
        print (S.snap_port)
        snap_opts = ' --host ' + S.snap_server + ' --port ' + S.snap_port
        S.stop_previous_instance()
        S.pro = subprocess.Popen(daemon + snap_opts, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    def _set_success_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_error_headers(self):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        params = parse_qs(self.path[2:])
        if 'url' in params:
            S.snap_server = params['url'][0]
        else:
            S.snap_server = default_snap_server
        if 'port' in params:
            S.snap_port = params['port'][0]
        else:
            S.snap_port = default_snap_port
        S.start_new_instance()
        self._set_success_headers()
        self.wfile.write('{"status":"success"}')

        
def run(server_class=HTTPServer, handler_class=S, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    S.start_new_instance()
    httpd.serve_forever()

def exit_handler():
    S.stop_previous_instance()

if __name__ == "__main__":
    from sys import argv

    atexit.register(exit_handler)

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
