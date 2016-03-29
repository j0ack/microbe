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
from microbe.utils import render
from microbe.mods.config.models import Config
from microbe.mods.content.models import Content, Tag, Category, Comment
from microbe.mods.content.forms import CommentForm
from microbe.mods.links.models import Link, LinkCategory
from microbe.mods.search.forms import SearchForm
from microbe.mods.email import send_email

from flask.ext.babel import format_datetime, lazy_gettext
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
    # posts categories
    g.categories = Category.query.all()
    # static pages
    g.static_pages = Content.query.filter_by(draft_status=False).filter_by(
        content_type='pages').all()
    # links
    g.links = Link.query.all()
    g.link_categories = LinkCategory.query.all()
    # search form
    if not hasattr(g, 'search_form'):
        g.search_form = SearchForm()


@frontend.route('/')
def index():
    """Main page of the app
    List of blog posts summaries
    """
    page = request.args.get('page', 1)
    per_page = current_app.config['PAGINATION']
    posts = Content.query.filter_by(draft_status=False).filter_by(
        content_type=u'posts')
    ordered_posts = posts.order_by(Content.published_date.desc()).paginate(
        page, per_page, False)
    return render('index.html', objects=ordered_posts)


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
        if current_app.config.get('COMMENTS', False):
            form = CommentForm()
    # form management
    if form and form.validate_on_submit():
        comment = Comment()
        comment.user = form.name.data
        comment.email = form.email.data
        comment.site = form.site.data
        comment.notif = form.notify.data
        comment.body = form.content.data
        comment.published_date = datetime.now()
        comment.content_id = content_id
        db.session.add(comment)
        db.session.commit()
        # contruct comment url
        content_url = urljoin(request.url_root, str(content.id))
        if content_url[:-1] != '/':
            content_url += '/'
        comment_url = content_url + '#' + str(comment.id)
        # contruct mail content
        sub = lazy_gettext(u'A new comment has been submitted')
        body = lazy_gettext(u'A new comment has been submitted to ')
        body += content.title
        body += '<br />'
        txt = lazy_gettext(u'See it online')
        body += '<a href="{}" title="comment">{}</a>'.format(comment_url, txt)
        recipients = []
        # notify author
        if content.author.email:
            recipients.append(content.author.email)
        # notify other commenters
        for com in content.comments:
            if com.notif and com.email:
                recipients.append(com.email)
        if recipients:
            send_email(sub, recipients, html_body=body)
    return render('page.html', page=content, form=form)


@frontend.route('/category/<category_id>')
def category(category_id):
    """Filter posts by category

    :param category: Category to filter contents
    """
    page = request.args.get('page', 1)
    per_page = current_app.config['PAGINATION']
    category = Category.query.get_or_404(category_id)
    contents = category.contents.paginate(page, per_page, False)
    return render('index.html', objects=contents, title=category.label)


@frontend.route('/tag/<tag_id>')
def tag(tag_id):
    """Filter posts by tag

    :param tag: Category to filter contents
    """
    page = request.args.get('page', 1)
    per_page = current_app.config['PAGINATION']
    tag = Tag.query.get_or_404(tag_id)
    contents = tag.contents.paginate(page, per_page, False)
    return render('index.html', objects=contents, title=tag.label)


@frontend.route('/archives')
def archives():
    """List all contents order by reverse date"""
    # sort pages by reverse date
    page = request.args.get('page', 1)
    pages = Content.query.filter_by(draft_status=False).order_by(
        Content.published_date.desc())
    paginate = pages.paginate(page, 10, False)
    return render('archive.html', objects=paginate)


@frontend.route('/search/', methods=['POST'])
def search():
    """Search in contents"""
    page = request.args.get('page', 1)
    if not g.search_form.validate_on_submit():
        return redirect(url_for('frontend.index'))
    query = g.search_form.search.data
    contents = Content.query.whoosh_search(query).filter_by(
        draft_status=False).paginate(page, 10, False)
    title = lazy_gettext('Results for "{}"'.format(query))
    return render('index.html', objects=contents, title=title)


@frontend.route('/feed.atom')
def feed():
    """Generate 20 last content atom feed"""
    if not current_app.config.get('RSS', False):
        abort(404)
    name = current_app.config['SITENAME']
    feed = AtomFeed(name, feed_url=request.url, url=request.url_root)
    posts = Content.query.filter_by(draft_status=False).filter_by(
        content_type=u'posts').order_by(Content.published_date.desc())
    # sort posts by reverse date
    for post in posts[:20]:
        feed.add(post.title,
                 unicode(post.summary),
                 content_type='html',
                 author=post.author.name,
                 url=urljoin(request.url_root, str(post.id)),
                 updated=post.published_date)
    return feed.get_response()


@frontend.route('/<content_id>/feed.atom')
def comments_feeds(content_id):
    """Generate content comments feeds
    :param content_id: content id
    """
    # check if RSS is enabled
    if not current_app.config.get('RSS', False):
        abort(404)
    # check if comments are enabled
    if not current_app.config.get('COMMENTS', False):
        abort(404)
    # check if content exists
    content = Content.query.get_or_404(content_id)
    name = u'Comments for ' + content.title
    feed = AtomFeed(name, feed_url=request.url, url=request.url_root)
    content_url = urljoin(request.url_root, str(content.id))
    if content_url[:-1] != '/':
        content_url += '/'
    # sort posts by reverse date
    for com in content.comments:
        feed.add(lazy_gettext(u'Comment for ') + content.title,
                 unicode(com.content),
                 content_type='html',
                 author=com.user,
                 url=urljoin(content_url, '#' + str(com.id)),
                 updated=com.published_date)
    return feed.get_response()
