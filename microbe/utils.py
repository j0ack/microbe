#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Utilities for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from itertools import islice
from flask import abort, render_template
from flask.ext.paginate import Pagination


def create_pagination(page, per_page, objects) :
    """
        Create Pagination objects

        :param page: current page number
        :param per_page: number of objects per page
        :param objects: list of objects
    """
    return Pagination(page = page, 
                      total = len(objects), 
                      search = False,
                      per_page = per_page,
                      css_framework='foundation')


def get_objects_for_page(page, per_page, objects) :
    """
        Calculate objects for paginated pages

        :param page: current page number
        :param per_page: number of objects per page
        :param objects: list of objects
    """
    # return empty list
    if not objects :
        return []
    # calculate index
    index_min = (page - 1) * per_page
    # if index minimum is more than objects length
    if index_min > len(objects) - 1 :
        abort(404)
    index_max = per_page * page
    # return a sliced list
    return list(islice(objects, index_min, index_max))


def merge_default_config(current_app) :
    """
        Populate config with default constant values
    """
    default = { 
            'CODEMIRROR_LANGUAGES' : [u'markdown'],
            'CODEMIRROR_THEME' : u'xq-light',
            'PERMANENT_SESSION_LIFETIME' : 2678400,
            'FLATPAGES_ROOT' : u'content',
            'POST_DIR' : u'posts',
            'PAGE_DIR' : u'pages',
            'FLATPAGES_EXTENSION' : u'.md',
            'FLATPAGES_AUTO_RELOAD' : True,
            'DEFAULT_THEME' : u'dark'
            }
    current_app.config.update(default)



def render_paginated(template, objects, per_page, request) :
    """
        Return a paginated template
        
        :param template: template to render
        :param page: current page number
        :param per_page: number of objects per page
        :param objects: list of objects
    """
    # get page from request
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    # create pagination
    pagination = create_pagination(page, per_page, objects)
    # calculate objects displayed
    displayed = get_objects_for_page(page, per_page, objects)
    # return
    return render_template(template, objects = displayed, 
                           pagination = pagination)

def truncate_markdown(markdown, length) :
    """
        Truncate markdown conserving opened tags

        If truncate in an opened tag will wait for closure

        :param markdown: markdown to truncate
        :param length: length to truncate
    """
    if not markdown :
        return ''
    if len(markdown) < length : 
        return markdown
    # truncate
    i = 0
    open_tag = False
    while i < length or open_tag :
        # increment counter
        i += 1
        # if a link is open
        if markdown[i] == '[' :
            open_tag = True
        # an image
        elif ( markdown[i] == '!' 
             and i < len(markdown) - 1 
             and markdown[i + 1] == '[' ) :
            open_tag = True
        # link closed
        elif markdown[i] == u')' :
            open_tag = False
    return markdown[:i+1] + '...'

