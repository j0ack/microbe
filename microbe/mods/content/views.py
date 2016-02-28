#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Contents views for Microbe app
"""

from datetime import datetime

from flask import render_template, redirect, request, url_for, jsonify
from flask.ext.login import current_user
from flask.ext.babel import lazy_gettext

from microbe.admin import admin
from microbe.database import db
from microbe.markdown_content import render_markdown
from microbe.mods.auth.decorator import auth_required
from microbe.mods.content.models import Content, Comment, Category, Tag
from microbe.mods.content.forms import ContentForm

__author__ = u'TROUVERIE Joachim'


@admin.route('/contents/')
@auth_required
def list_contents():
    """List contents"""
    page = request.args.get('page', 1)
    contents = Content.query.order_by(
        Content.published_date.desc()).paginate(page, 15, False)
    return render_template('admin/contents.html', objects=contents)


@admin.route('/render/', methods=['POST'])
@auth_required
def render():
    """Render markdown"""
    content = request.form.get('content', '')
    return jsonify(value=render_markdown(content))


@admin.route('/delete_content/', methods=['POST'])
@auth_required
def delete_content():
    """Delete content"""
    uid = request.form['content']
    content = Content.query.get_or_404(uid)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('admin.list_contents'))


@admin.route('/publish_content/', methods=['POST'])
@auth_required
def publish_content():
    """Publish content"""
    uid = request.form['content']
    content = Content.query.get_or_404(uid)
    content.draft_status = False
    db.session.commit()
    return redirect(url_for('admin.list_contents'))


@admin.route('/content/<content_id>/', methods=['GET', 'POST'])
@admin.route('/content/', methods=['GET', 'POST'])
@auth_required
def content(content_id=None):
    """Edit or create post"""
    # edit post
    if content_id:
        title = lazy_gettext(u'Edit content')
        content = Content.query.get_or_404(content_id)
        form = ContentForm(obj=content)
    else:
        title = lazy_gettext(u'New content')
        content = Content()
        content.published_date = datetime.now()
        form = ContentForm()
    # populate form
    if form.validate_on_submit():
        # populate obj
        content.title = form.title.data
        content.body = form.body.data
        content.content_type = form.content_type.data
        # category
        name = form.category.data
        category = Category.query.filter_by(label=name).first()
        if not category:
            category = Category(label=form.category.data)
            db.session.add(category)
        content.category = category
        if content.category_id and content.category_id != category.id:
            category = Category.query.get(content.category_id)
            category.contents.remove(content)
            if len(category.contents.all()) == 0:
                db.session.delete(category)
        # deleted tags
        for tag in content.tags:
            if tag.label not in form.tags.data:
                tag.contents.remove(content)
                if len(tag.contents.all()) == 0:
                    db.session.delete(tag)
        # added tags
        for name in form.tags.data.split(','):
            tag_name = name.strip()
            tag = Tag.query.filter_by(label=tag_name).first()
            if not tag:
                tag = Tag(label=tag_name)
                db.session.add(tag)
            if tag not in content.tags:
                content.tags.append(tag)
        content.draft_status = True
        content.author_id = current_user.id
        if not content_id:
            db.session.add(content)
        db.session.commit()
        return redirect(url_for('admin.list_contents'))
    # new post
    return render_template('admin/content.html', title=title,
                           url=url_for('admin.content', content_id=content_id),
                           form=form)


@admin.route('/comments/<content_id>/')
@auth_required
def comments(content_id):
    """List comments for a content
    Available action is delete
    """
    # get comments
    page = request.args.get('page', 1)
    content = Content.query.get_or_404(content_id)
    comments = content.comments.order_by(
        Comment.publised_date.desc()).paginate(page, 15, False)
    return render_template('admin/comments.html',
                           content_id=content_id, comments=comments)


@admin.route('/delete_comment/', methods=['POST'])
@auth_required
def delete_comment():
    """Delete a comment"""
    # get comment id
    comment_id = request.form['comment']
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    if len(comment.content.comments.all()) > 0:
        content_id = comment.content.id
        return redirect(url_for('admin.comments', content_id=content_id))
    else:
        return redirect(url_for('admin.list_contents'))
