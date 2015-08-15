#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    FlatContent module for Microbe app

    Sub-class of FlatPages extension to add
    concurrent access management
"""

import itertools
import os.path
from lockfile import LockFile as lock

from flask.ext.flatpages import FlatPages

from microbe.flatcontent.models import Content


__author__ = 'TROUVERIE Joachim'


class FlatContent(FlatPages):
    """Override of FlatPages for Microbe"""
    def _parse(self, content, path):
        """
            Return an instance of `Content` instead of `Page`
        """
        lines = iter(content.split(u'\n'))
        # Read lines until an empty line is encountered.
        meta = u'\n'.join(itertools.takewhile(unicode.strip, lines))
        # The rest is the content. `lines` is an iterator so it continues
        # where `itertools.takewhile` left it.
        content = u'\n'.join(lines)
        return Content(path, meta, content)

    def _load_file(self, path, filename):
        """
            Implements of lockfile
        """
        mtime = os.path.getmtime(filename)
        cached = self._file_cache.get(filename)
        if cached and cached[1] == mtime:
            page = cached[0]
        else:
            with lock(filename):
                with open(filename) as fd:
                    content = fd.read().decode(self.config('encoding'))
            page = self._parse(content, path)
            self._file_cache[filename] = page, mtime
        return page
