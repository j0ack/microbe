#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Config model
"""

from microbe.database import db


__author__ = 'TROUVERIE Joachim'


class Config(db.Model):
    """Config model"""
    __tablename__ = 'Config'

    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    language = db.Column(db.String(2))
    author = db.Column(db.String(50))
    pagination = db.Column(db.Integer)
    summary_length = db.Column(db.Integer)
    comments = db.Column(db.Boolean)
    rss = db.Column(db.Boolean)
    recaptcha_public_key = db.Column(db.String(40))
    recaptcha_private_key = db.Column(db.String(40))

    def __repr__(self):
        return u'<Config>'

    def to_dict(self):
        return self.__dict__
