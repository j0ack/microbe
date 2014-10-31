#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
   Commands for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

import os
import sys
import os.path as op
import json
from zipfile import ZipFile
from argparse import ArgumentParser
from cherrypy import wsgiserver

from microbe import app
from microbe.mods.search import init_index

def runserver(args) :
    """
        Run Microbe app on CherrPy server
        
        :param ip: Host to serve the app
        :param port: Port to host the app
        :param url: Sub-url to host the app
        :type ip: str
        :type port: int
        :type url: str
    """
    init_index()
    url = args.url
    host = args.ip
    port = args.port
    debug = args.debug
    if not debug :
        d = wsgiserver.WSGIPathInfoDispatcher({url: app.wsgi_app}) 
        server = wsgiserver.CherryPyWSGIServer((host, port), d)
        server.start()
    else :
        app.debug = True
        app.run(port=port)
    

def reinit(args) :
    """
        Reinit microbe config
    """
    msg = 'Are you sure to reinit microbe config ? [Y/N]'
    # get input from user
    letter = None
    while not letter :
        letter = raw_input(msg)
        if letter.lower() not in ['y','n'] :
            print 'Invalid choice'
            letter = None
        elif letter.lower() == 'y' :
            path = app.config['SHELVE_FILENAME']
            os.remove(path)
            print '{0} has been removed'.format(path)
        else :
            sys.exit(1)

    
def save(args) :
    """
        Save microbe config and contents in a ZIP file
        
        :param output: Output file name
        :type output: str
    """
    output = args.output
    # create zip object
    with ZipFile(output, 'w') as zf :
        # add all pages
        root_path = op.dirname(__file__)
        path = op.join(root_path, app.config['FLATPAGES_ROOT'])
        for root, dirs, files in os.walk(path):
            for file in files :
                filepath = op.join(root, file)
                zf.write(filepath, filepath.replace(root_path, ''))
        # media
        path = op.join(op.dirname(__file__), 'static', 'media')
        for root, dirs, files in os.walk(path):
            for file in files :
                filepath = op.join(root, file)
                zf.write(filepath, filepath.replace(root_path, ''))
        # add config
        path = app.config['SHELVE_FILENAME']
        zf.write(path, 'config.db')
    print 'Zip file created'
        
    
def restore(args) :
    """
        Restore microbe config and contents from a ZIP file
        
        :param input: Input file path
        :type input: str
    """
    infile = args.input
    root_path = op.dirname(__file__)
    # check if valid
    if op.exists(infile) :
        with ZipFile(infile, 'r') as zf :
            zf.extractall(root_path)
        print 'Zip file restored'
    else :
        print '{0} does not exists'.format(infile)
                

def theme_skeleton(args) :
    """
        Create a theme skeletton for Microbe

        :param theme: Theme name
        :param author: Author name
    """
    theme = args.theme
    author = args.author
    path = op.join(op.dirname(__file__), 'themes', theme)
    if not op.exists(path) :
        os.makedirs(op.join(path, 'templates'))
        os.makedirs(op.join(path, 'static', 'js'))
        os.makedirs(op.join(path, 'static', 'css'))
        os.makedirs(op.join(path, 'static', 'img'))
        with open(op.join(path, 'info.json'), 'w') as info :
            json.dump({
                'application' : 'microbe',
                'identifier' : theme,
                'name': theme,
                'author': author,
                'licence' : 'your-licence',
                'description' : 'a description',
                'version' : '0.0.1',
                'preview' : 'a screenshot to save in static folder'
            }, info, indent=4, separators=(',',': '))
        # templates
        open(op.join(path, 'templates', 'index.html'), 'a').close()
        open(op.join(path, 'templates', 'page.html'), 'a').close()
        open(op.join(path, 'templates', 'archive.html'), 'a').close()
        open(op.join(path, 'templates', '404.html'), 'a').close()
        print 'Theme created, you can edit your files at {0}'.format(path)
    else :
        print 'This theme already exists delete it first'


def main() :
    """
        Launchers for Microbe app
    """
    # create main parser
    parser = ArgumentParser('Microbe')
    subparsers = parser.add_subparsers()
    # run command
    run_parser = subparsers.add_parser('runserver', help='Run Microbe app server')
    run_parser.add_argument('-i', '--ip', default='127.0.0.1', help='Host to deploy app')
    run_parser.add_argument('-p', '--port', default=8000, type=int, help='Port to deploy app')
    run_parser.add_argument('-u', '--url', default='/', help='Url to deploy app')
    run_parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    run_parser.set_defaults(func=runserver)
    # reinit command
    reinit_parser = subparsers.add_parser('reinit', help='Reinit Microbe app config')
    reinit_parser.set_defaults(func=reinit)
    # save command
    save_parser = subparsers.add_parser('save', help='Save Microbe app config and contents')
    save_parser.add_argument('-o', '--output', default='microbe.zip', help='Output ZIP file')
    save_parser.set_defaults(func=save)
    # restore command
    restore_parser = subparsers.add_parser('restore', help='Restore Microbe app config and contents')
    restore_parser.add_argument('input', help='Input ZIP file (created by microbe save)')
    restore_parser.set_defaults(func=restore)
    # theme command
    theme_parser = subparsers.add_parser('theme', help='Create theme skeleton')
    theme_parser.add_argument('theme', help='Theme name')
    theme_parser.add_argument('author', help='Your name')
    theme_parser.set_defaults(func=theme_skeleton)
    # parse
    args = parser.parse_args()
    # lanch command
    args.func(args)
