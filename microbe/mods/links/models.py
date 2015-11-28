#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Link models for Microbe app
"""


from microbe.database import db

__author__ = u'TROUVERIE Joachim'


class Link(db.Model):
    """Links model"""
    __tablename__ = 'Link'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    url = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('LinkCategory.id'))
    category = db.relationship('LinkCategory',
                               backref=db.backref('links', lazy='dynamic'))

    def __init__(self, label, url, category):
        self.label = label
        self.url = url
        self.category = category

    def __repr__(self):
        return '<Link label={} url={}>'.format(self.label, self.url)

    @property
    def html(self):
        """Html reprensentation"""
        _template = u'<a href="{}" class="{}" id="{}">{}</a>'
        return _template.format(self.url, self.category.name,
                                self.id, self.label)


class LinkCategory(db.Model):
    """Links category"""
    __tablename__ = 'LinkCategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Link category {}>'.format(self.name)
