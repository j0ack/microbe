#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Classes for Microbe app
"""

__author__ = 'TROUVERIE Joachim'

import os
import re
from os.path import join, splitext
from uuid import uuid4
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from yaml import safe_dump

from flask import current_app, url_for
from flask.ext.flatpages import Page, pygmented_markdown
from flask.ext.login import current_user

from utils import truncate_markdown

class Users(object) :
    """
        Users API class providing static methods to work with users
    """
    @staticmethod
    def get(username) :
        """
            Get user by username
        """
        # get password hash for username
        dic = current_app.config[u'USERS']
        pwd_hash = dic.get(username)
        if not pwd_hash :
            return None
        # create object
        return User(username, pwd_hash, True)


    @staticmethod
    def delete(username) :
        """
            Delete user by username
        """
        # get config
        dic = current_app.config[u'USERS']
        # delete entry
        del dic[username]
        # update config
        current_app.config.update({ u'USERS' : dic })


    @staticmethod 
    def update(username, password) :
        """
            Add or update a user
        """
        # get config
        dic = current_app.config[u'USERS']
        # create object
        user = User(username, password)
        # create new entry or update value
        dic[username] = user.pw_hash
        # update config
        current_app.config.update({ u'USERS' : dic })


class User(object) :
    """
        User class

        :param name: user name
        :param password: user password
        :param hashed: if the given password is hashed
        :type name: str
        :type password: str
        :type hashed: bool
    """
    def __init__(self, name, password, hashed = False):
        self.name = name
        # hash password if necessary
        if not hashed :
            self.pw_hash = generate_password_hash(password)
        else :
            self.pw_hash = password


    def check_password(self, password) :
        """
            Check password hash

            :param password: clear password to check
            :type password: str
        """
        return check_password_hash(self.pw_hash, password)


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return unicode(self.name)
    

class Links(object) :
    """
        Links API provide static method to deal with static links
    """
    @staticmethod
    def get_all() :
        """
            Get all links from config
        """
        # get all config keys starting with MICROBELINKS_
        links = {
                key.replace(u'MICROBELINKS_', '') : values
                for key, values in current_app.config.iteritems()
                if key.startswith(u'MICROBELINKS_')
                }
        objects = {}
        # create Link object from values
        for key, values in links.iteritems() :
            objects[key] = []
            for tup in values :
                objects[key].append(
                        Link(tup[0], tup[1], tup[2], tup[3])
                )
        return objects


    @staticmethod
    def add(label, url, category) :
        """
            Add a new link

            :param label: link label which is displayed
            :param url: link url
            :param category: link category
        """
        # create a new key from link category
        key = u'MICROBELINKS_' + category.upper()
        links = current_app.config.get(key, [])
        # append a new link
        links.append((
                label,
                url,
                category,
                uuid4().hex
            ))
        # update config
        current_app.config.update({key : links})


    @staticmethod
    def delete(link_id) :
        """
            Delete a link from its id
        """
        # get all config keys starting with MICROBELINKS_
        links = {
                key : values
                for key, values in current_app.config.iteritems()
                if key.startswith(u'MICROBELINKS_')
                }
        # get link with given id
        for key, values in links.iteritems() :
            objects = values
            for value in values :
                if value[3] == link_id :
                    # remove object
                    objects.remove(value)
                    # update config
                    current_app.config.update({key : objects})
                    break

            

class Link(object) :
    """
        Static link class

        :param label: link label
        :param url: link url
        :param category: link category
        :param uid: link id, if not provided will be calculated by uid4()
    """
    def __init__(self, label, url, category, uid = None) :
        if not uid :
            self.uid = uuid4().hex
        else :
            self.uid = uid
        self.label     = label
        self.url       = url
        self.category  = category

    
    @property
    def html(self) :
        """
            Render used by Jinja2 templates
        """
        _template = u'<a href="{}" class="{}" id="{}">{}</a>'
        return _template.format(self.url, self.category, 
                                    self.uid, self.label)


class File(object) :
    """
        Media file object

        :param filename: file name
    """
    def __init__(self, filename) :
        self.name = filename


    @property
    def url(self) :
        """
            File url
        """
        return url_for('static', filename = '/media/' + self.name)


    @property
    def slug(self) :
        """
            File name without ext
        """
        return splitext(self.name)[0]


class Comment(object) :
    """
        Comment class    

        :param author: comment author
        :param date: str comment date using format %d-%m-%Y %H:%M
        :param content: comment content
        :param uid: comment id, if not provided will be calculated by uid4()
    """
    def __init__(self, author, date, content, uid = None) :
        if not uid : 
            self.uid = uuid4().hex
        else :
            self.uid = uid
        self.author = author
        self.content = content
        self.date = datetime.strptime(date, u'%d-%m-%Y %H:%M')


class Content(Page) :
    """
        Override of flatpages Page class
    """
    def __init__(self, path = None, meta = '', body = None) :
        if not meta :
            meta_dict = { u'draft' : True }
            meta = safe_dump(meta_dict)
        super(Content, self).__init__(path, meta, body, pygmented_markdown)


    @staticmethod
    def from_page(page) :
        """
            Construct object from flat page
            :param page: Page to construct from
            :type page: Page
        """
        return Content(page.path, page._meta_yaml, page.body)


    @property
    def title(self) :
        return self.meta.get(u'title')


    @title.setter
    def title(self, title) :
        self._setmeta(u'title', title)


    @property
    def tags(self) :
        return self.meta.get(u'tags')


    @tags.setter
    def tags(self, tags) :
        val = ','.join([t.strip() for t in tags.split(',')])
        self._setmeta(u'tags', val)


    @property
    def category(self) :
        return self.meta.get(u'category')


    @category.setter
    def category(self, category) :
        self._setmeta(u'category', category) 


    @property
    def content_type(self) :
        return self.meta.get(u'content_type')


    @content_type.setter
    def content_type(self, content_type) :
        self._setmeta(u'content_type', content_type)


    @property
    def draft(self) :
        return self.meta.get(u'draft')


    @draft.setter
    def draft(self, draft) :
        self._setmeta(u'draft', draft)

    
    @property
    def summary(self) :
        """
            A truncated version of content
        """
        max_length = current_app.config[u'SUMMARY_LENGTH']
        markdown = truncate_markdown(self.body, max_length)
        return self.html_renderer(markdown)

    
    @property
    def published(self) :
        if self.meta.get(u'published'):
            return datetime.strptime(
                    self.meta.get(u'published'),
                    u'%d-%m-%Y'
            )
        return None 


    @published.setter
    def published(self, date) :
        self._setmeta(u'published', datetime.strftime(date, u'%d-%m-%Y'))


    @property
    def comments(self) :
        lst = []
        comments = self.meta.get(u'comments', [])
        for author, date, content, uid in comments :
            lst.append(Comment(author, date, content, uid))
        return sorted(lst, key = lambda x : x.date)


    def _setmeta(self, name, value) :
        """
            Set meta values directly
        """
        meta = self.meta
        meta[name] = value
        self._meta_yaml = safe_dump(meta)


    def add_comment(self, author, content) :
        """
            Add comment to post
        """
        # get meta
        meta = self.meta
        # check if comments exists in meta
        comments = meta.get(u'comments', [])         
        comments.append((
            author,
            datetime.now().strftime(u'%d-%m-%Y %H:%M'),
            content,
            uuid4().hex
        ))
        # save
        meta[u'comments'] = comments
        self._meta_yaml = safe_dump(meta)
        self.save()


    def delete_comment(self, uid) :
        """
            Delete a comment
        """
        meta = self.meta
        comments = self.comments
        for com in comments :
            if com.uid == uid :
                comments.remove(com)
                break
        # save
        meta[u'comments'] = comments
        self._meta_yaml = safe_dump(meta)
        self.save()


    def _construct_path(self) :
        """
            Construct path from type and title
        """
        title = self.meta.get(u'title')
        content_type = self.meta.get(u'content_type')
        # construct
        value = re.sub('[^\w\s-]', '', title).strip().lower()
        slug = re.sub('[-\s]+', '-', value)
        return join(content_type, slug) 


    def save(self) :
        """
            Save file
        """
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = join(root, flat_pages_root)
        # check path
        path = self._construct_path()
        if self.path and self.path != path :
            # delete file
            self.delete()
        # update config
        if not self.published :
            self.published = datetime.now()
        if not self.meta.get(u'author') :
            self._setmeta(u'author', current_user.get_id())
        self.path = path
        final_path = join(root_path, self.path) + u'.md'
        # save in file
        with open(final_path, 'w') as sa :
            sa.write(self._meta_yaml.encode(u'utf-8'))
            sa.write('\n')
            sa.write(self.body.encode(u'utf-8'))


    def delete(self) :
        """
            Delete file
        """
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = join(root, flat_pages_root)
        os.remove(join(root_path, self.path) + u'.md')
