#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Link views for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from itertools import chain

from flask import url_for, redirect, render_template, request
from flask.ext.login import login_required
from flask.ext.babel import lazy_gettext

from microbe.utils import render_list
from microbe.admin import admin
from microbe.mods.links.forms import LinkForm
from microbe.mods.links.models import Links


@admin.route('/links/')
@login_required
def links() :
    """
        List of links
    """
    # get config
    lst = Links.get_all()
    links = list(chain.from_iterable(lst.values()))
    return render_list('admin/links.html', links, per_page=15)

    
@admin.route('/delete_link/', methods = ['POST'])
@login_required
def delete_link() :
    """
        Delete link
    """
    # delete a link
    link = request.form['link']
    Links.delete(link)
    # update config
    return redirect(url_for('admin.links'))

    
@admin.route('/link/', methods = ['GET', 'POST'])
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
        return redirect(url_for('admin.links'))
    return render_template('admin/model.html', title = title, 
            form = form, url = url_for('admin.link'))
