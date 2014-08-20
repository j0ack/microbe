#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Views for Microbe app
"""

__author__ = 'TROUVERIE Joachim'

import os.path
import shelve
from datetime import datetime
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin

from microbe import app, contents, babel
from models import Links
from forms import CommentForm, SearchForm
from utils import render_theme_paginated
from search import search_query 

from flask.ext.babel import format_datetime, lazy_gettext
from flask.ext.themes2 import render_theme_template, static_file_url
from flask import (g, request, abort, url_for, make_response, 
                  render_template, redirect)

def render(template, **context):
    """
        Render template with config theme
        instead of default theme
    """
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    return render_theme_template(theme, template, **context)


@app.errorhandler(404)
def page_not_found(e):
    """
        Page not found error handler
    """
    return render('404.html'), 404


@babel.localeselector
def get_locale() :
    """
        Get locale for page translations
    """
    return app.config.get(u'LANGUAGE')


@app.template_filter('date')
def date_filter(date, format = None) :
    """
        Date filter to use in Jinja2 templates

        :param date : datetime object to convert
        :param format: format to convert date object
        :type date: datetime
        :type format: str

        .. warnings:: Format is in flask.ext.babel format
    """
    if date :
        if format :
            return format_datetime(date, format)
        else :
            return format_datetime(date, 'dd MM yyyy')
    else :
        return ''


@app.before_request
def before_request() :
    """
        Refresh global vars before each requests
    """
    # update config
    path = app.config['SHELVE_FILENAME']
    db = shelve.open(path)
    app.config.update(db)
    # posts list    
    g.posts  = sorted(
                [c for c in contents if c.content_type == 'posts' 
                and not c.draft],
                key = lambda x : x.published,
                reverse = True
                )
    # posts categories
    g.categories = set([c.category for c in g.posts if c.category])
    # static pages
    g.static_pages = [c for c in contents if c.content_type == 'pages'
                     and not c.draft]
    # links
    g.links = Links.get_all()
    # search form
    if not hasattr(g, 'search_form') : 
        g.search_form = SearchForm()
    # close db
    db.close()


@app.route('/')
def index():
    """
        Main page of the app

        List of blog posts summaries
    """
    # theme
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    # per page
    per_page = app.config['PAGINATION']
    return render_theme_paginated('index.html', theme, g.posts, per_page,
                                    request) 


@app.route('/sitemap.xml')
def sitemap() :
    """
        Site sitemap
    """
    # list all contents
    sitemap_contents = [c for c in contents if not c.draft]
    sitemap = render_template('sitemap.xml', contents = sitemap_contents)
    response = make_response(sitemap)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/favicon.ico')
def favicon() :
    """
        App favicon
    """
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    try :
        return static_file_url(theme, 'img/favicon.png')
    except :
        return url_for('static', filename='img/favicon.png')


@app.route('/<path:path>/', methods = ['GET', 'POST'])
def page(path):
    """
        Get access for page from its path.
        If path is not valid it will return a 404 error page

        :param path: Valid content path 
    """    
    content = contents.get_or_404(path)
    form = None
    # enable comments for posts only
    if content.content_type == 'posts' :
        form = CommentForm()
    # form management
    if form and form.validate_on_submit() :
        author = form.name.data
        body = form.content.data
        content.add_comment(author, body)
    return render('page.html', page = content, form = form)


@app.route('/category/<category>')
def category(category) :
    """
        Filter posts by category

        :param category: Category to filter contents
        :type category: str
    """
    posts = [p for p in g.posts if p.category == category]
    # theme
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    # per page
    per_page = app.config['PAGINATION']
    return render_theme_paginated('index.html', theme, posts, per_page,
                                    request, title=category)


@app.route('/tag/<tag>')
def tag(tag) :
    """
        Filter posts by tag

        :param tag: Category to filter contents
        :type tag: str
    """
    posts = [p for p in g.posts if tag in p.tags.split(',')]
    # theme
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    # per page
    per_page = app.config['PAGINATION']
    return render_theme_paginated('index.html', theme, posts, per_page,
                                    request, title=tag)


@app.route('/archives')
def archives() :
    """
       List all contents order by reverse date
    """
    # sort pages by reverse date
    sorted_pages = sorted(
                        contents,
                        key = lambda x : x.published,
                        reverse = True
                    )
    # theme
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    return render_theme_paginated('archive.html', theme, sorted_pages, 10,
                                    request)


@app.route('/search/', methods = ['POST'])
def search() :
    """
        Search in contents
    """
    if not g.search_form.validate_on_submit() :
        return redirect(url_for('index'))
    query = g.search_form.search.data
    contents = search_query(query)
    # sort not draft contents by reverse date
    sorted_contents = sorted(
                            [c for c in contents if not c.draft], 
                            key = lambda x : x.published,
                            reverse = True
                       )
    # pagination
    # theme
    default = app.config['DEFAULT_THEME']
    theme = app.config.get(u'THEME', default)
    return render_theme_paginated('index.html', theme, sorted_contents, 
                                    10, request, title=query)

    
@app.route('/feed.atom')
def feed() :
    """
        Generate 20 last content atom feed
    """
    if app.config.get('RSS', 'NO') != 'YES' :
        abort(404)
    name = app.config['SITENAME']
    feed = AtomFeed(name,feed_url=request.url, url=request.url_root)
    # sort posts by reverse date
    for post in g.posts[:20] :
        feed.add( post.meta.get(u'title'),
                unicode(post.summary),
                content_type = 'html',
                author = post.meta.get('author', ''),
                url = urljoin(request.url_root, post.path),
                updated = post.published)
    return feed.get_response()
