#! /urs/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Commands for Microbe
"""

import os
import os.path as op
import json
from flask.ext.script import Manager, Command, Option, prompt, prompt_bool
from flask.ext.babel import lazy_gettext
from microbe import app
from utils import merge_default_config
from search import init_index

# create manager
manager = Manager(app)

class CherryPyServer(Command) :
    """
        Serve Microbe app
    
        :param host: Host to serve the app
        :param port: Port to host the app
        :param suburl: Sub-url to host the app
        :param debug: Debug mode
        :type host: str
        :type port: int
        :type suburl: str
        :type debug: bool
    """
    def __init__(self, host=u'127.0.0.1', port=8000, suburl=u'/', debug=False) :
        self.host = host
        self.port = port
        self.suburl = suburl
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
            Option('-s', '--suburl',
                    dest='suburl',
                    type=str,
                    default=self.suburl),
            Option('-d', '--debug',
                    dest='debug',
                    type=bool,
                    default=self.debug)
        )


    def run(self, host, port, suburl, debug) :
        """
            Run server
        """
        init_index()
        if not debug :
            from cherrypy import wsgiserver
            d = wsgiserver.WSGIPathInfoDispatcher({suburl: app.wsgi_app}) 
            server = wsgiserver.CherryPyWSGIServer((host, port), d)
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
    msg = lazy_gettext(u'Are you sure to reinit microbe config ?')
    if prompt_bool(msg) :
        path = app.config['SHELVE_FILENAME']
        if os.path.exists(path) :
            os.remove(path)
        merge_default_config(app.config)


@manager.command
def theme_skeleton() :
    """
        Create theme minimal skeleton
    """
    # name
    msg = lazy_gettext(u'Enter your theme name')
    name = prompt(msg)
    # path
    path = op.join(op.abspath(op.dirname(__file__)), 'themes', name)
    if not op.exists(path) :
        os.makedirs(op.join(path, 'templates'))
        os.makedirs(op.join(path, 'static', 'js'))
        os.makedirs(op.join(path, 'static', 'css'))
        os.makedirs(op.join(path, 'static', 'img'))
        # author
        msg = lazy_gettext(u'Enter your name')
        author = prompt(msg)
        # json
        with open(op.join(path, 'info.json'), 'w') as info :
            json.dump({
                 "application": "microbe",
                 "identifier": name,
                 "name": name,
                 "author": author,
                 "license": "your license here",
                 "description": "a small description",
                 "version": "0.0.1",
                 "preview": "a screenshot to save in static dir"
            }, info, indent=4, separators=(',', ': '))
        # templates
        open(op.join(path, 'templates', 'index.html'), 'a').close()
        open(op.join(path, 'templates', 'archive.html'), 'a').close()
        open(op.join(path, 'templates', 'page.html'), 'a').close()
        open(op.join(path, 'templates', '404.html'), 'a').close()
    else :
        msg = lazy_gettext(u'This theme already exists delete it first')
        print msg


def main() :
    manager.run()


if __name__ == '__main__' : 
    main()
