#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    FlatContent models for Microbe app
"""

from datetime import datetime
from hashlib import md5
from urlparse import urljoin

from flask import current_app

from microbe.database import db
from microbe.markdown_content import render_markdown
from microbe.utils import truncate_html_words

__author__ = u'TROUVERIE Joachim'

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id')),
                db.Column('content_id', db.Integer, db.ForeignKey('Content.id'))
)


class Content(db.Model):
    __tablename__ = 'Content'
    __searchable__ = ['body', 'title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    content_type = db.Column(db.String(5))
    draft_status = db.Column(db.Boolean)
    published_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    comments = db.relationship('Comment', backref='content', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('contents', lazy='dynamic'))

    def __repr__(self):
        date = datetime.strftime(self.published_date, u'%d-%m-%Y')
        return '<{0} {1}>'.format(self.content_type, date)

    @property
    def html(self):
        """HTML repr"""
        return render_markdown(self.body)

    @property
    def summary(self):
        """HTML content summary"""
        length = current_app.config['SUMMARY_LENGTH']
        return truncate_html_words(self.html, length)


class Tag(db.Model):
    __tablename__ = 'Tag'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Tag {0}>'.format(self.label)


class Category(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True)
    contents = db.relationship('Content', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {0}>'.format(self.label)


class Comment(db.Model):
    __tablename__ = 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    email = db.Column(db.String(50))
    site = db.Column(db.String(50))
    notif = db.Column(db.Boolean)
    published_date = db.Column(db.DateTime)
    body = db.Column(db.Text())
    content_id = db.Column(db.Integer, db.ForeignKey('Content.id'))

    def __repr__(self):
        date = datetime.strftime(self.published_date, u'%d-%m-%Y')
        return '<Comment {0} {1}>'.format(self.user, date)

    @property
    def avatar(self):
        """Gravatar support"""
        url = u'http://www.gravatar.com/avatar/'
        code = md5(self.email.encode('utf-8')).hexdigest()
        par = u'{0}?d=retro'.format(code)
        return urljoin(url, par)
