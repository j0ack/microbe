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

from microbe import app, contents, babel
from models import Links
from forms import CommentForm, SearchForm
from utils import get_objects_for_page, create_pagination
from search import search_query 

from flask import g, request, abort, url_for
from flask.ext.babel import format_datetime, lazy_gettext
from flask.ext.themes2 import render_theme_template


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
    # pagination
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    per_page = app.config['PAGINATION']
    pagination = create_pagination(page, per_page, g.posts)
    # get content for current page
    displayed = get_objects_for_page(page, per_page, g.posts)
    # override page to have summary
    return render('index.html', pages=displayed, pagination=pagination)


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
    # pagination
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    per_page = app.config['PAGINATION']
    pagination = create_pagination(page, per_page, posts)
    # get content for current page
    displayed = get_objects_for_page(page, per_page, posts)
    return render('index.html', title = category, pages = displayed,
            pagination = pagination)


@app.route('/tag/<tag>')
def tag(tag) :
    """
        Filter posts by tag

        :param tag: Category to filter contents
        :type tag: str
    """
    posts = [p for p in g.posts if tag in p.tags.split(',')]
    # pagination
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    per_page = app.config['PAGINATION']
    pagination = create_pagination(page, per_page, posts)
    # get content for current page
    displayed = get_objects_for_page(page, per_page, posts)
    return render('index.html', title = tag, pages = displayed,
            pagination = pagination)


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
    # pagination
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    per_page = 10   
    pagination = create_pagination(page, per_page, sorted_pages)
    # get content for current page
    displayed = get_objects_for_page(page, per_page, sorted_pages)
    return render('archive.html',  pages = displayed, 
            pagination = pagination)


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
    try :
        page = int(request.args.get('page', 1))
    except ValueError :
        page = 1
    per_page = 20    
    pagination = create_pagination(page, per_page, sorted_contents)
    # get content for current page
    displayed = get_objects_for_page(page, per_page, sorted_contents)
    return render('index.html', title = query, pages = displayed,
            pagination = pagination)

    


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
                url = url_for('page', path = post.path, _external = True),
                updated = post.published)
    return feed.get_response()
