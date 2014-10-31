#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    FlatContent models for Microbe app
"""

__author__ = 'TROUVERIE Joachim'

import os.path as op
import re
from uuid import uuid4
from lockfile import LockFile as lock
from datetime import datetime
from yaml import safe_dump

from flask.ext.flatpages import Page
from flask.ext.login import current_user
from flask import current_app

from microbe.utils import truncate_html_words
from microbe.markdown_content import render_markdown

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
        Override of Page for Microbe
    """
    def __init__(self, path = None, meta = '', body = None) :
        if not meta :
            meta_dict = { u'draft' : True }
            meta = safe_dump(meta_dict)
        super(Content, self).__init__(path, meta, body, render_markdown)

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
        length = current_app.config.get('SUMMARY_LENGTH')
        content = self.html_renderer(self.body)
        return truncate_html_words(content, length)

    
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
        return op.join(content_type, slug) 


    def save(self) :
        """
            Save file
        """
        root = current_app.root_path
        flat_pages_root = current_app.config.get(u'FLATPAGES_ROOT')
        root_path = op.join(root, flat_pages_root)
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
        final_path = op.join(root_path, self.path) + u'.md'
        # save in file
        with lock(final_path) :
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
        root_path = op.join(root, flat_pages_root)
        os.remove(op.join(root_path, self.path) + u'.md')
