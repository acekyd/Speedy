import logging
from threading import Thread
from flask import Flask

flask: Flask = Flask('replit_keep_alive')
log: logging.Logger = logging.getLogger('werkzeug')

@flask.route('/')
def index() -> str:
    """Method for handling the base route of '/'."""
    return "Keeping the repl alive!"

def keep_alive() -> None:
    """Wraps the web server run() method in a Thread object and starts the web server."""
    def run() -> None:
        log.setLevel(logging.ERROR)
        flask.run(host = '0.0.0.0', port = 8080)
    thread = Thread(target = run)
    thread.start()