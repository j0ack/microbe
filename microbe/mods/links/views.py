#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Link views for Microbe app
"""


from flask import url_for, redirect, render_template, request
from flask.ext.babel import lazy_gettext

from microbe.admin import admin
from microbe.database import db
from microbe.mods.auth.decorator import auth_required
from microbe.mods.links.forms import LinkForm
from microbe.mods.links.models import Link, LinkCategory

__author__ = u'TROUVERIE Joachim'


@admin.route('/links/')
@auth_required
def links():
    """List of links"""
    page = request.args.get('page', 1)
    links = Link.query.paginate(page, 15, False)
    return render_template('admin/links.html', objects=links)


@admin.route('/delete_link/', methods=['POST'])
@auth_required
def delete_link():
    """Delete link"""
    link_id = request.form['link']
    link = Link.query.get_or_404(link_id)
    category = link.category
    # only one link in category
    if len(category.links.all()) == 1:
        db.session.delete(link.category)
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for('admin.links'))


@admin.route('/link/', methods=['GET', 'POST'])
@auth_required
def link():
    """Create a new link"""
    form = LinkForm()
    title = lazy_gettext(u'New link')
    if form.validate_on_submit():
        # add new link
        label = form.label.data
        url = form.url.data
        cat = form.category.data
        # get category or create it
        category = LinkCategory.query.filter_by(name=cat).first()
        if not category:
            category = LinkCategory(cat)
        link = Link(label, url, category)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('admin.links'))
    return render_template('admin/model.html', title=title,
                           form=form, url=url_for('admin.link'))
