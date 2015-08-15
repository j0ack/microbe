#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users models for Microbe app
"""

import os.path as op

from flask import url_for

__author__ = 'TROUVERIE Joachim'


class File(object):
    """Media file object

    :param filename: file name
    """
    def __init__(self, filename):
        self.name = filename

    @property
    def url(self):
        """File url"""
        return url_for('static', filename='media/' + self.name)

    @property
    def slug(self):
        """File name without ext"""
        return op.splitext(self.name)[0]
