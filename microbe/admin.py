#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Admin BluePrint for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

import os
import os.path as op
from datetime import datetime
from itertools import chain
from werkzeug import secure_filename

from microbe import contents
from flatcontent import Content
from models import Users, File, Links 
from search import update_document, delete_document
from utils import render_paginated
from forms import LoginForm, UserForm, ConfigForm, ContentForm, LinkForm

from flask import (Blueprint, url_for, redirect, current_app, request,
                   render_template, jsonify)
from flask.ext import shelve
from flask.ext.themes2 import get_themes_list
from flask.ext.babel import lazy_gettext, refresh
from flask.ext.login import login_user, logout_user, login_required

# create blueprint
bp = Blueprint('admin', __name__)


def load_user(username) :
    """
        Load user from config

        :param username: user name
        :type username: str
    """
    # get config
    config = current_app.config['USERS']
    return Users.get(username)


@bp.route('/')
@login_required
def index() :
    """
        Admin index view
    """
    return render_template('admin/index.html')


@bp.route('/login', methods = ['GET', 'POST'])
def login() :
    """
        Login page
    
        Will log the user to allow the access for 
        blueprint views
    """
    # create form
    form = LoginForm()
    # form submit
    if form.validate_on_submit() :
        # check username and password
        user = Users.get(form.username.data)
        if not user :
            form.username.errors.append(lazy_gettext(u'Invalid user'))
        elif not user.check_password(form.password.data) :
            form.password.errors.append(lazy_gettext(u'Invalid password'))
        else :
            login_user(user, remember = form.remember.data)
            return redirect(url_for('.index'))
    return render_template('admin/model.html', form = form, 
            url = url_for('.login'))


@bp.route('/logout')
@login_required
def logout() :
    """
        Logout the current user
    """
    logout_user()
    return redirect(url_for('index'))


@bp.route('/config', methods = ['GET', 'POST'])
@login_required
def config() :
    """
        Edit app config from form
    """
    # get config
    db = shelve.get_shelve('w')
    config = db
    # populate form with config
    form = ConfigForm(
            server_name = config.get(u'SERVER_NAME'),
            sitename = config.get(u'SITENAME'),
            subtitle = config.get(u'SUBTITLE'),
            author = config.get(u'AUTHOR'),
            language = config.get(u'LANGUAGE'),
            pagination = config.get(u'PAGINATION'),
            summary_length = config.get(u'SUMMARY_LENGTH'),
            comments = config.get(u'COMMENTS'),
            rss = config.get(u'RSS'),
            recaptcha_public_key = config.get(u'RECAPTCHA_PUBLIC_KEY'),
            recaptcha_private_key = config.get(u'RECAPTCHA_PRIVATE_KEY')
            )
    if form.validate_on_submit() :
        # refresh babel
        if config.get(u'LANGUAGE') != db.get(u'LANGUAGE') :
            refresh()
        db['SERVER_NAME'] = form.server_name.data
        db['SITENAME'] = form.sitename.data
        db['SUBTITLE'] = form.subtitle.data
        db['AUTHOR'] = form.author.data
        db['LANGUAGE'] = form.language.data
        db['PAGINATION'] = form.pagination.data
        db['SUMMARY_LENGTH'] = form.summary_length.data
        db['COMMENTS'] = form.comments.data
        db['RSS'] = form.rss.data
        db['RECAPTCHA_PUBLIC_KEY'] = form.recaptcha_public_key.data
        db['RECAPTCHA_PRIVATE_KEY'] = form.recaptcha_private_key.data
        return redirect(url_for('admin.index'))
    return render_template('admin/model.html', 
            form = form, 
            title = lazy_gettext(u'Configuration of ') + 
            config.get(u'SITENAME'),
            url = url_for('.config'))


@bp.route('/users/', methods = ['GET', 'POST'])
@login_required
def users() :
    """
        List users

        Available actions are edit, delete or add
    """
    # delete a user
    db = shelve.get_shelve('r')
    if request.method == 'POST' :
        user = request.form['user']
        Users.delete(user)
    users = db['USERS']
    lst = users.keys()
    return render_paginated('admin/users.html', lst, 15, request)


@bp.route('/user/<user>', methods = ['GET', 'POST'])
@bp.route('/user/', methods = ['GET', 'POST'])
@login_required
def user(user = None) :
    """
        Edit or create user
    """
    # get user
    if user :
        form = UserForm(username = user)
        title = user
    else :
        form = UserForm()
        title = lazy_gettext(u'New user')
    if form.validate_on_submit() :
        # update or add new user
        username = form.username.data
        pwd = form.password.data
        Users.update(username, pwd)
        return redirect(url_for('.users'))
    return render_template('admin/model.html', title = title, 
            form = form, url = url_for('.user'))

@bp.route('/links/', methods = ['GET', 'POST'])
@login_required
def links() :
    """
        List of links

        Available actions are add or delete
    """
    # delete a link
    if request.method == 'POST' :
        link = request.form['link']
        Links.delete(link)
    # get config
    lst = Links.get_all()
    links = list(chain.from_iterable(lst.values()))
    return render_paginated('admin/links.html', links, 15, request)


@bp.route('/link/', methods = ['GET', 'POST'])
@login_required
def link() :
    """
        Create a new link
    """
    form = LinkForm()
    title = lazy_gettext(u'New link')
    if form.validate_on_submit() :
        # add new link
        label = form.label.data
        url = form.url.data
        cat = form.category.data
        Links.add(label, url, cat)
        return redirect(url_for('.links'))
    return render_template('admin/model.html', title = title, 
            form = form, url = url_for('.link'))


@bp.route('/contents/', methods = ['GET', 'POST'])
@login_required
def contents() :
    """
        List contents

        Available actions are edit, add and delete
    """
    # delete a content
    if request.method == 'POST' :
        path = request.form['path']
        delete = request.form.get('delete')
        content = [c for c in contents if c.path == path][0]
        # delete
        if delete :
            contents.remove(content)
            content.delete()
            delete_document(content)
        # publish
        else :
            content.draft = False
            content.published = datetime.now()
            content.save()
            update_document(content)
    # get   
    sorted_contents = sorted(contents, 
                             key = lambda x : x.published,
                             reverse = True)
    return render_paginated('admin/contents.html', sorted_contents, 15, 
                            request)


@bp.route('/content/<path:path>/', methods = ['GET', 'POST'])
@bp.route('/content/', methods = ['GET', 'POST'])
@login_required
def content(path = None) :
    """
        Edit or create post
    """    
    # edit post
    if path :
        title = lazy_gettext(u'Edit content')
        content = contents.get(path)
    else :
        content = Content()
        title = lazy_gettext(u'New content')
    # populate form
    form = ContentForm(obj = content)
    if form.validate_on_submit() :
        form.populate_obj(content)
        content.save()
        update_document(content)
        return redirect(url_for('.contents'))
    # new post
    return render_template('admin/content.html', title = title, 
            url = url_for('.content'), form = form)


@bp.route('/comments/<path:path>/', methods = ['GET', 'POST'])
@login_required
def comments(path) :
    """
        List comments for a content

        Available action is delete
    """
    # delete a comment
    if request.method == 'POST' :
        comment = request.form['comment']
        content = contents.get(path)
        content.delete_comment(comment)
    # get comments
    page = contents.get(path)
    content = Content.from_page(page)
    comments = content.comments
    return render_paginated('admin/comments.html', comments, 15, request)


@bp.route('/media/', methods = ['GET', 'POST'])
@login_required
def media() :
    """
        List media available to contents
    """
    path = op.join(op.abspath(op.dirname(__file__)), 'static', 'media')
    if not op.exists(path) :
        os.makedirs(path)
    files = [File(f) for f in os.listdir(path)]
    # delete a file
    if request.method == 'POST' :
        slug = request.form['slug']
        for fi in files :
            if fi.slug == slug :
                files.remove(fi)
                filepath = op.join(path, fi.name)
                os.remove(filepath)
    return render_paginated('admin/media.html', files, 15, request)


@bp.route('/upload/', methods = ['POST'])
@login_required
def upload() :
    """
        Upload new file
    """
    path = op.join(op.abspath(op.dirname(__file__)), 'static', 'media')
    fi = request.files[u'file']
    if fi :
        filename = secure_filename(fi.filename)
        path = op.join(path, filename)
        fi.save(path)
        # request sent by ajax
        if request.is_xhr :
            obj = File(op.basename(path))
            return jsonify(
                        url = obj.url,
                        slug = obj.slug,
                        label = obj.name
                    )
        else :
            return redirect(url_for('.media'))
    return None


@bp.route('/themes/')
@login_required
def themes() :
    """
        List available themes
    """
    db = shelve.get_shelve('r')
    current_app.theme_manager.refresh()
    themes = get_themes_list()
    default_theme = db['DEFAULT_THEME']
    selected = db.get(u'THEME', default_theme)
    return render_template('admin/themes.html', themes = themes, 
            selected = selected)


@bp.route('/themes/<ident>')
@login_required
def set_theme(ident):
    """
        Set theme in config to be displayed to users
    """
    db = shelve.get_shelve('w')
    if ident not in current_app.theme_manager.themes :
        abort(404)
    db['THEME'] = ident
    return redirect(url_for('.themes'))
