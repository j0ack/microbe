#! /urs/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Commands for Microbe
"""

import os
from flask.ext.script import Manager, Command, Option
from microbe import app
from search import init_index

# create manager
manager = Manager(app)


class CherryPyServer(Command) :
    """
        Use CherryPy server instead of Flask built in server

        :param host: Host to serve the app
        :param port: Port to host the app
        :param debug: Debug mode
        :type host: str
        :type port: int
        :type debug: bool
    """
    def __init__(self, host=u'127.0.0.1', port=8000, debug=False) :
        self.host = host
        self.port = port
        self.debug = debug


    def get_options(self) :
        """
            Get options for the command
        """
        return (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),
            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),
            Option('-d', '--debug',
                   dest='debug',
                   type=bool,
                   default=self.debug)
        )


    def run(self, host, port, debug) :
        """
            Run server
        """
        init_index()
        if not debug :
            from cherrypy import wsgiserver
            server = wsgiserver.CherryPyWSGIServer((host, port), app)
            print u'App served on {0}:{1}'.format(host, port)
            server.start()
        else :
            app.config['DEBUG'] = True
            app.run(port=port)


manager.add_command("runserver", CherryPyServer())                

@manager.command
def reinit() :
    """
        Reinit Microbe config
    """
    path = app.config['SHELVE_FILENAME']
    if os.path.exists(path) :
        os.remove(path)


def main() :
    manager.run()
