#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Comments views for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from flask import redirect, url_for, request
from flask.ext.login import login_required

from microbe import contents
from microbe.admin import admin
from microbe.utils import render_list

@admin.route('/comments/<path:path>/')
@login_required
def comments(path) :
    """
        List comments for a content

        Available action is delete
    """
    # get comments
    content = contents.get(path)
    comments = content.comments
    return render_list('admin/comments.html', comments, per_page=15)


@admin.route('/delete_comment/<path:path>/', methods=['POST'])
@login_required    
def delete_comment(path) :
    """
        Delete a comment
        
    """
    # get comment id
    comment = request.form['comment']
    # get content    
    content = contents.get(path)
    # delete comment
    content.delete_comment(comment)
    return redirect(url_for('admin.comments'))
        