#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    FlatContent models for Microbe app
"""

import os
import os.path as op
import re

from hashlib import md5
from uuid import uuid4
from datetime import datetime
from yaml import safe_dump, YAMLObject, load_all, dump_all
from urlparse import urljoin

from flask.ext.flatpages import Page
from flask.ext.login import current_user
from flask import current_app, url_for

from microbe.utils import truncate_html_words, load_file, save_file
from microbe.markdown_content import render_markdown
from microbe.mods.email import send_email
from microbe.mods.users.models import Users

__author__ = 'TROUVERIE Joachim'


class Comment(YAMLObject):
    """Comment class

    :param author: comment author
    :param date: str comment date using format %d-%m-%Y %H:%M
    :param content: comment content
    :param email: comment author email
    :param uid: comment id, if not provided will be calculated by uid4()
    """
    yaml_tag = u'!Comment'

    def __init__(self, author, date, content, email, site, notif, uid=None):
        if not uid:
            self.uid = uuid4().hex
        else:
            self.uid = uid
        self.author = author
        self.email = email
        self.site = site
        self.notif = notif
        self.content = content
        self.date = date

    def __repr__(self):
        """YAML representation"""
        date = self.date.strftime('%d-%m-%Y %H:%M')
        rep = u'{0}(uid={1},author={2},content={3},date={4},email={5},site={6},notif={7})'
        return rep.format(self.__class__.__name__, self.uid, self.author,
                          self.content, date, self.email, self.site,
                          self.notif)

    @property
    def avatar(self):
        """Gravatar support"""
        url = u'http://www.gravatar.com/avatar/'
        par = u'{0}?d=retro'.format(md5(self.email.encode('utf-8')).hexdigest())
        return urljoin(url, par)


class Content(Page):
    """Override of Page for Microbe"""
    def __init__(self, path=None, meta='', body=None):
        self._com_mtime = None
        self._comments = []
        if not meta:
            meta_dict = {u'draft': True}
            meta = safe_dump(meta_dict)
        super(Content, self).__init__(path, meta, body, render_markdown)

    @property
    def title(self):
        return self.meta.get(u'title')

    @title.setter
    def title(self, title):
        self._setmeta(u'title', title)

    @property
    def tags(self):
        return self.meta.get(u'tags')

    @tags.setter
    def tags(self, tags):
        val = ','.join([t.strip() for t in tags.split(',')])
        self._setmeta(u'tags', val)

    @property
    def category(self):
        return self.meta.get(u'category')

    @category.setter
    def category(self, category):
        self._setmeta(u'category', category)

    @property
    def content_type(self):
        return self.meta.get(u'content_type')

    @content_type.setter
    def content_type(self, content_type):
        self._setmeta(u'content_type', content_type)

    @property
    def draft(self):
        return self.meta.get(u'draft')

    @draft.setter
    def draft(self, draft):
        self._setmeta(u'draft', draft)

    @property
    def summary(self):
        """A truncated version of content"""
        length = current_app.config.get('SUMMARY_LENGTH')
        content = self.html_renderer(self.body)
        return truncate_html_words(content, length)

    @property
    def published(self):
        if self.meta.get(u'published'):
            return datetime.strptime(
                self.meta.get(u'published'),
                u'%d-%m-%Y'
            )
        return None

    @published.setter
    def published(self, date):
        self._setmeta(u'published', datetime.strftime(date, u'%d-%m-%Y'))

    @property
    def comments(self):
        # comment path
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = op.join(root, flat_pages_root)
        comments_path = op.join(root_path, 'comments')
        final_path = op.join(comments_path, self.slug)
        lst = []
        # load from file
        if op.exists(final_path):
            mtime = op.getmtime(final_path)
            if not self._com_mtime or mtime != self._com_mtime:
                stream = load_file(final_path)
                lst = load_all(stream)
                self._com_mtime = op.getmtime(final_path)
                self._comments = sorted(lst, key=lambda x: x.date)
        return self._comments or []

    @property
    def slug(self):
        """Title slug"""
        title = self.meta.get(u'title')
        value = re.sub('[^\w\s-]', '', title).strip().lower()
        slug = re.sub('[-\s]+', '-', value)
        return slug

    def _setmeta(self, name, value):
        """Set meta values directly"""
        meta = self.meta
        meta[name] = value
        self._meta_yaml = safe_dump(meta)

    def _save_comments(self):
        """Save comments in a file"""
        # comment path
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = op.join(root, flat_pages_root)
        comments_path = op.join(root_path, 'comments')
        final_path = op.join(comments_path, self.slug)
        # get stream
        stream = dump_all(self._comments)
        save_file(stream, final_path)

    def add_comment(self, author, email, site, content, notif):
        """Add comment to post
        :param author: comment's author
        :param email: comment's author email
        :param site: comment's author site
        :param content: comment's content
        :param notif: notify user of new comments
        """
        comment = Comment(author, datetime.now(), content, email, site, notif)
        self._comments.append(comment)
        # dump
        stream = dump_all(self._comments)
        self._save_comments()
        # notification
        url = url_for('frontend.page', path=self.path)
        msg = 'There is a new comment for this '
        msg += '<a href="{0}" target="_blank">post</a>'.format(url)
        # collect all emails
        emails = [com.email for com in self._comments if com.notif and com.uid != comment.uid]
        author = Users.get(self.meta.get(u'author'))
        if author.email:
            emails.append(email)
        send_email(u'New_comment', emails, None, msg)

    def delete_comment(self, uid):
        """Delete a comment by its uid
        :param uid: Comment's uid
        """
        self._comments = [com for com in self._comments if com.uid != uid]
        self._save_comments()

    def _construct_path(self):
        """Construct path from type and title"""
        content_type = self.meta.get(u'content_type')
        return op.join(content_type, self.slug)

    def save(self):
        """Save file"""
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = op.join(root, flat_pages_root)
        # check path
        path = self._construct_path()
        if self.path and self.path != path:
            # delete file
            self.delete()
        # update config
        if not self.published:
            self.published = datetime.now()
        if not self.meta.get(u'author'):
            self._setmeta(u'author', current_user.get_id())
        self.path = path
        final_path = op.join(root_path, self.path) + u'.md'
        # save in file
        content = self._meta_yaml.encode(u'utf-8')
        content += '\n'
        content += self.body.encode(u'utf-8')
        save_file(content, final_path)

    def delete(self):
        """Delete file"""
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = op.join(root, flat_pages_root)
        os.remove(op.join(root_path, self.path) + u'.md')
