#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Comments views for Microbe app
"""

from flask import redirect, url_for, request
from flask.ext.login import login_required

from microbe import contents
from microbe.admin import admin
from microbe.utils import render_list

__author__ = 'TROUVERIE Joachim'


@admin.route('/comments/<path:path>/')
@login_required
def comments(path):
    """List comments for a content
    Available action is delete
    """
    # get comments
    content = contents.get(path)
    comments = content.comments
    return render_list('admin/comments.html', comments, per_page=15, path=path)


@admin.route('/delete_comment/<path:path>/', methods=['POST'])
@login_required
def delete_comment(path):
    """Delete a comment"""
    # get comment id
    comment = request.form['comment']
    # get content
    content = contents.get(path)
    # delete comment
    content.delete_comment(comment)
    if len(content.comments) > 0:
        return redirect(url_for('admin.comments', path=path))
    else:
        return redirect(url_for('admin.list_contents'))
