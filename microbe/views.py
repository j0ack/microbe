#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Views for Microbe app
"""

import os.path as op
import xml.etree.ElementTree as ET
from datetime import datetime
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin

from microbe import babel
from microbe.database import db
from microbe.utils import render, render_list
from microbe.mods.config.models import Config
from microbe.mods.content.models import Content, Tag, Category, Comment
from microbe.mods.content.forms import CommentForm
from microbe.mods.links.models import Link
from microbe.mods.search.forms import SearchForm

from flask.ext.babel import format_datetime
from flask.ext.themes2 import static_file_url, get_theme
from flask import (Blueprint, current_app, g, request, abort, url_for,
                   make_response, redirect)

__author__ = 'TROUVERIE Joachim'


frontend = Blueprint('frontend', __name__)


def page_not_found(e):
    """Page not found error handler"""
    return render('404.html'), 404


@babel.localeselector
def get_locale():
    """Get locale for page translations"""
    return current_app.config.get('LANGUAGE')


@frontend.app_template_filter('date')
def date_filter(date, format=None):
    """Date filter to use in Jinja2 templates

    :param date : datetime object to convert
    :param format: format to convert date object
    :type date: datetime
    :type format: str

    .. warnings:: Format is in flask.ext.babel format
    """
    if date:
        if format:
            return format_datetime(date, format)
        else:
            return format_datetime(date, 'dd MM yyyy')
    else:
        return ''


@frontend.before_app_request
def before_request():
    """Refresh global vars before each requests"""
    # update config
    config = Config.query.first()
    if config:
        current_app.config.update(config.to_dict())
    # posts list
    g.posts = Content.query.filter_by(draft_status=False).filter_by(
        content_type='posts').order_by(Content.published_date.desc()).all()
    # posts categories
    g.categories = Category.query.all()
    # static pages
    g.static_pages = Content.query.filter_by(draft_status=False).filter_by(
        content_type='pages').all()
    # links
    g.links = Link.query.all()
    # search form
    if not hasattr(g, 'search_form'):
        g.search_form = SearchForm()


@frontend.route('/')
def index():
    """Main page of the app
    List of blog posts summaries
    """
    return render_list('index.html', g.posts)


@frontend.route('/sitemaps.xml')
def sitemap():
    """Site sitemap"""
    # list all contents
    sitemap_contents = Content.query.filter_by(draft_status=False).all()
    # root
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    for content in sitemap_contents:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = urljoin(request.url_root, content.path)
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = format_datetime(content.published, 'yyyy-MM-dd')
    text = ET.tostring(root)
    response = make_response(text, 200)
    response.headers['Content-Type'] = 'application/xml'
    return response


@frontend.route('/favicon.ico')
def favicon():
    """App favicon"""
    default = current_app.config['DEFAULT_THEME']
    theme_id = current_app.config.get(u'THEME', default)
    theme = get_theme(theme_id)
    path = op.join(theme.static_path, 'img', 'favicon.png')
    if op.exists(path):
        url = static_file_url(theme, 'img/favicon.png')
    else:
        url = url_for('static', filename='img/favicon.png')
    return redirect(url)


@frontend.route('/robots.txt')
def robots():
    """App robots.txt"""
    try:
        url = url_for('static', filename='media/robots.txt')
        return redirect(url)
    except:
        abort(404)


@frontend.route('/<content_id>/', methods=['GET', 'POST'])
def page(content_id):
    """Get access for page from its id.
    If path is not valid it will return a 404 error page

    :param path: Valid content path
    """
    content = Content.query.get_or_404(content_id)
    form = None
    # enable comments for posts only
    if content.content_type == 'posts':
        if current_app.config.get('COMMENTS', 'NO') == 'YES':
            form = CommentForm()
    # form management
    if form and form.validate_on_submit():
        comment = Comment()
        comment.user = form.name.data
        comment.email = form.email.data
        comment.site = form.site.data
        comment.notif = form.notify.data
        comment.published_date = datetime.now()
        comment.content_id = content_id
        db.session.add(comment)
        db.session.commit()
    return render('page.html', page=content, form=form)


@frontend.route('/category/<category_id>')
def category(category_id):
    """Filter posts by category

    :param category: Category to filter contents
    """
    page = request.args('page', 1)
    per_page = current_app.config['PAGINATION']
    category = Category.query.get_or_404(category_id)
    contents = category.contents.paginate(page, per_page, False)
    return render('index.html', contents, title=category.label)


@frontend.route('/tag/<tag_id>')
def tag(tag_id):
    """Filter posts by tag

    :param tag: Category to filter contents
    """
    page = request.args('page', 1)
    per_page = current_app.config['PAGINATION']
    tag = Tag.get_or_404(tag_id)
    contents = tag.contents.paginate(page, per_page, False)
    return render('index.html', contents, title=tag.label)


@frontend.route('/archives')
def archives():
    """List all contents order by reverse date"""
    # sort pages by reverse date
    page = request.args.get('page', 1)
    sorted_pages = Content.filter_by(draft_status=False).order_by(
        Content.published_date.desc()).paginate(page, 10, False)
    return render('archive.html', sorted_pages)


@frontend.route('/search/', methods=['POST'])
def search():
    """Search in contents"""
    page = request.args.get('page', 1)
    if not g.search_form.validate_on_submit():
        return redirect(url_for('frontend.index'))
    query = g.search_form.search.data
    contents = Content.query.filter_by(draft_status=False).whoosh_search(
        query).paginate(page, 10, False)
    return render('index.html', contents)


@frontend.route('/feed.atom')
def feed():
    """Generate 20 last content atom feed"""
    if current_app.config.get('RSS', 'NO') != 'YES':
        abort(404)
    name = current_app.config['SITENAME']
    feed = AtomFeed(name, feed_url=request.url, url=request.url_root)
    # sort posts by reverse date
    for post in g.posts[:20]:
        feed.add(post.title,
                 unicode(post.summary),
                 content_type='html',
                 author=post.meta.get('author', ''),
                 url=urljoin(request.url_root, post.path),
                 updated=post.published)
    return feed.get_response()


@frontend.route('/<content_id>/feed.atom')
def comments_feeds(content_id):
    """Generate content comments feeds
    :param content_id: content id
    """
    # check if RSS is enabled
    if current_app.config.get('RSS', 'NO') != 'YES':
        abort(404)
    # check if comments are enabled
    if current_app.config.get('COMMENTS', 'NO') != 'YES':
        abort(404)
    # check if content exists
    content = Content.get_or_404(content_id)
    name = u'Comments for ' + content.title
    feed = AtomFeed(name, feed_url=request.url, url=request.url_root)
    content_url = urljoin(request.url_root, content.id)
    if content_url[:-1] != '/':
        content_url += '/'
    # sort posts by reverse date
    for com in content.comments:
        feed.add(u'Comment for ' + content.title,
                 unicode(com.content),
                 content_type='html',
                 author=com.author,
                 url=urljoin(content_url, '#' + com.id),
                 updated=com.date)
    return feed.get_response()
