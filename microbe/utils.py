#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Utilities for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

import os.path
import re
import shelve
from itertools import islice

from flask import abort, request, current_app
from flask.ext.paginate import Pagination
from flask.ext.themes2 import render_theme_template
from werkzeug.security import generate_password_hash

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


def merge_default_config(config) :
    """
        Populate config with default constant values
    """
    path = config.get(u'SHELVE_FILENAME')
    db = shelve.open(path, 'c')
    db['LANGUAGE'] = u'en'
    db['SITENAME'] = u'Microbe Default site'
    db['USERS'] = {u'admin' : generate_password_hash(u'microbe')}
    db['POST_DIR'] = u'posts'
    db['PAGE_DIR'] = u'pages'
    db['PAGINATION'] = 5
    db['SUMMARY_LENGTH'] = 300
    db['COMMENTS'] = u'NO'
    db['RSS'] = u'NO'
    db['DEFAULT_THEME'] = u'dark'
    db.close()

                           
def render(template, **context):
    """
        Render template with config theme
        instead of default theme
    """
    default = current_app.config['DEFAULT_THEME']
    theme = current_app.config.get('THEME', default)
    return render_theme_template(theme, template, **context)
    
    
def render_list(template, list, **context) :
    """
        Render list with pagination with config theme
        instead of default theme
    """
    # get page from request
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    # per page
    per_page = context.get('per_page', current_app.config['PAGINATION'])
    # create pagination
    pagination = create_pagination(page, per_page, list)
    # calculate objects displayed
    displayed = get_objects_for_page(page, per_page, list)
    # get theme
    default = current_app.config['DEFAULT_THEME']
    theme = current_app.config.get('THEME', default)
    # return
    return render_theme_template(theme, template, objects = displayed, 
                               pagination = pagination, **context)
                           

def truncate_html_words(s, num, end_text='...'):
    """
        Truncates HTML to a certain number of words.

        (not counting tags and comments). Closes opened tags if they were correctly
        closed in the given html. Takes an optional argument of what should be used
        to notify that the string has been truncated, defaulting to ellipsis (...).

        Newlines in the HTML are preserved. (From the django framework).
    """
    length = int(num)
    if length <= 0:
        return ''
    html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area',
                      'hr', 'input')

    # Set up regular expressions
    re_words = re.compile(r'&.*?;|<.*?>|(\w[\w-]*)', re.U)
    re_tag = re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
    # Count non-HTML words and keep note of open tags
    pos = 0
    end_text_pos = 0
    words = 0
    open_tags = []
    while words <= length:
        m = re_words.search(s, pos)
        if not m:
            # Checked through whole string
            break
        pos = m.end(0)
        if m.group(1):
            # It's an actual non-HTML word
            words += 1
            if words == length:
                end_text_pos = pos
            continue
        # Check for tag
        tag = re_tag.match(m.group(0))
        if not tag or end_text_pos:
            # Don't worry about non tags or tags after our truncate point
            continue
        closing_tag, tagname, self_closing = tag.groups()
        tagname = tagname.lower() # Element names are always case-insensitive
        if self_closing or tagname in html4_singlets:
            pass
        elif closing_tag:
            # Check for match in open tags list
            try:
                i = open_tags.index(tagname)
            except ValueError:
                pass
            else:
                # SGML: An end tag closes, back to the matching start tag,
                # all unclosed intervening start tags with omitted end tags
                open_tags = open_tags[i + 1:]
        else:
            # Add it to the start of the open tags list
            open_tags.insert(0, tagname)
    if words <= length:
        # Don't try to close tags if we don't need to truncate
        return s
    out = s[:end_text_pos]
    if end_text:
        out += ' ' + end_text
    # Close any tags still open
    for tag in open_tags:
        out += '</%s>' % tag
    # Return string
    return out


