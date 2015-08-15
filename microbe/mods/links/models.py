#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Link models for Microbe app
"""

import shelve
from uuid import uuid4

from flask import current_app

__author__ = 'TROUVERIE Joachim'


class Links(object):
    """Links API provide static method to deal with static links"""
    @staticmethod
    def get_all():
        """Get all links from config"""
        # get all config keys starting with MICROBELINKS_
        links = {key.replace('MICROBELINKS_', ''): values
                 for key, values in current_app.config.iteritems()
                 if key.startswith('MICROBELINKS_')}
        objects = {}
        # create Link object from values
        for key, values in links.iteritems():
            objects[key] = []
            for tup in values:
                objects[key].append(Link(tup[0], tup[1], tup[2], tup[3]))
        return objects

    @staticmethod
    def add(label, url, category):
        """Add a new link

        :param label: link label which is displayed
        :param url: link url
        :param category: link category
        """
        # create a new key from link category
        path = current_app.config['SHELVE_FILENAME']
        db = shelve.open(path)
        key = 'MICROBELINKS_' + str(category.upper())
        links = db.get(key, [])
        # append a new link
        links.append((label,
                      url,
                      category,
                      uuid4().hex))
        # update config
        db[key] = links
        db.close()

    @staticmethod
    def delete(link_id):
        """Delete a link from its id"""
        # get all config keys starting with MICROBELINKS_
        path = current_app.config['SHELVE_FILENAME']
        db = shelve.open(path)
        links = {key: values
                 for key, values in db.iteritems()
                 if key.startswith('MICROBELINKS_')}
        # get link with given id
        for key, values in links.iteritems():
            objects = values
            for value in values:
                if value[3] == link_id:
                    # remove object
                    objects.remove(value)
                    # update config
                    db[key] = objects
                    break
        db.close()


class Link(object):
    """Static link class

    :param label: link label
    :param url: link url
    :param category: link category
    :param uid: link id, if not provided will be calculated by uid4()
    """
    def __init__(self, label, url, category, uid=None):
        if not uid:
            self.uid = uuid4().hex
        else:
            self.uid = uid
        self.label = label
        self.url = url
        self.category = category

    @property
    def html(self):
        """Render used by Jinja2 templates"""
        _template = u'<a href="{}" class="{}" id="{}">{}</a>'
        return _template.format(self.url, self.category,
                                self.uid, self.label)
