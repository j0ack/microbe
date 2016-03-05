#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users views for Microbe app
"""

import os.path as op
import os
from werkzeug import secure_filename

from flask import (current_app, redirect, url_for, request, jsonify,
                   render_template)
from flask.ext.babel import lazy_gettext

from microbe.admin import admin
from microbe.mods.auth.decorator import auth_required
from microbe.mods.media.models import File

__author__ = 'TROUVERIE Joachim'


@admin.route('/media/', methods=['GET', 'POST'])
@auth_required
def media():
    """List media available to contents"""
    path = op.join(current_app.root_path, 'static', 'media')
    if not op.exists(path):
        os.makedirs(path)
    files = [File(f) for f in os.listdir(path)]
    # delete a file
    return render_template('admin/media.html', objects=files)


@admin.route('/delete-file/', methods=['POST'])
@auth_required
def delete_file():
    """Delete a file"""
    path = op.join(current_app.root_path, 'static', 'media')
    files = [File(f) for f in os.listdir(path)]
    slug = request.form['slug']
    for fi in files:
        if fi.slug == slug:
            files.remove(fi)
            filepath = op.join(path, fi.name)
            os.remove(filepath)
    return redirect(url_for('admin.media'))


@admin.route('/upload/', methods=['POST'])
@auth_required
def upload():
    """Upload new file"""
    path = op.join(current_app.root_path, 'static', 'media')
    fi = request.files[u'file']
    if fi:
        filename = secure_filename(fi.filename)
        path = op.join(path, filename)
        fi.save(path)
        obj = File(op.basename(path))
        if request.is_xhr:
            return jsonify(url=obj.url,
                           slug=obj.slug,
                           label=obj.name)
        else:
            return redirect(url_for('admin.media'))
    return jsonify(error=lazy_gettext('Error uploading file'))
