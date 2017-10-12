#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'David Gilson (Gilsdav)'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import subprocess
import os
import atexit
import signal

import logging
import logging.handlers
import argparse
import sys


# Defaults
NAME = 'snapclient'
DAEMON = '/usr/bin/' + NAME

DEFAULT_SNAP_PORT = '1704'
DEFAULT_SNAP_SERVER = '127.0.0.1'


### Logger ###

# Log Defaults
LOG_FILENAME = "/tmp/snapclient-switcher.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Snapclient switcher service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)


### Switcher ###

class Switcher(BaseHTTPRequestHandler):

    pro = None
    snap_server = DEFAULT_SNAP_SERVER
    snap_port = DEFAULT_SNAP_PORT

    @staticmethod
    def stop_previous_instance():
        if not (Switcher.pro is None):
            Switcher.pro.kill()
            pid = subprocess.check_output('pidof snapclient', shell=True).strip()
            subprocess.call('kill ' + pid, shell=True)

    @staticmethod
    def start_new_instance():
        print('New connection : ' + Switcher.snap_server + ':' + Switcher.snap_port)
        snap_opts = ' --host ' + Switcher.snap_server + ' --port ' + Switcher.snap_port
        Switcher.stop_previous_instance()
        Switcher.pro = subprocess.Popen(DAEMON + snap_opts,
                                        stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

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
            Switcher.snap_server = params['url'][0]
        else:
            Switcher.snap_server = DEFAULT_SNAP_SERVER
        if 'port' in params:
            Switcher.snap_port = params['port'][0]
        else:
            Switcher.snap_port = DEFAULT_SNAP_PORT
        Switcher.start_new_instance()
        self._set_success_headers()
        self.wfile.write('{"status":"success"}')


def run(server_class=HTTPServer, handler_class=Switcher, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting snapclient-switcher v' + __version__ + ' ...')
    Switcher.start_new_instance()
    httpd.serve_forever()

def exit_handler():
    print('Stopping snapclient-switcher ...')
    Switcher.stop_previous_instance()

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)


if __name__ == "__main__":
    from sys import argv

    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
