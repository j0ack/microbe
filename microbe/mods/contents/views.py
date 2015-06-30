#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Contents views for Microbe app 
"""

from flask import render_template, redirect, request, url_for, jsonify
from flask.ext.login import login_required
from flask.ext.babel import lazy_gettext

from microbe import contents
from microbe.markdown_content import render_markdown
from microbe.utils import render_list
from microbe.admin import admin
from microbe.flatcontent.forms import ContentForm
from microbe.flatcontent.models import Content
from microbe.mods.search import delete_document, update_document

@admin.route('/contents/')
@login_required
def list_contents() :
    """
        List contents
    """
    # get   
    sorted_contents = sorted(contents, 
                             key = lambda x : x.published,
                             reverse = True)
    return render_list('admin/contents.html', sorted_contents, per_page=15)


@admin.route('/render/', methods=['POST'])
@login_required
def render() :
    """
        Render markdown
    """
    content = request.form.get('content','')
    return jsonify(value=render_markdown(content))
                            
                            
@admin.route('/delete_content/', methods=['POST'])
@login_required
def delete_content() :
    """
        Delete content
    """
    path = request.form['path']
    content = [c for c in contents if c.path == path][0]
    content.delete()
    delete_document(content)
    return redirect(url_for('admin.list_contents'))


@admin.route('/publish_content/', methods=['POST'])
@login_required
def publish_content() :
    """
        Publish content
    """
    path = request.form['path']
    content = [c for c in contents if c.path == path][0]
    content.draft = False
    content.save()
    update_document(content)
    return redirect(url_for('admin.list_contents'))
    
    
@admin.route('/content/<path:path>/', methods = ['GET', 'POST'])
@admin.route('/content/', methods = ['GET', 'POST'])
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
        # populate obj
        form.populate_obj(content) 
        content.draft = True
        content.save()
        update_document(content)
        return redirect(url_for('admin.list_contents'))
    # new post
    return render_template('admin/content.html', title = title, 
            url = url_for('admin.content', path=path), form = form)
