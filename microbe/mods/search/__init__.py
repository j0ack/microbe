#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Search module for Microbe app
"""

import os.path as op
import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser

from microbe import contents

__author__ = 'TROUVERIE Joachim'

# global index writer
global _ix


def init_index():
    """Init the index"""
    global _ix
    # create index writer at the launch
    path = op.join(op.dirname(__file__), 'index')
    # schema
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True, unique=True),
                    content=TEXT)
    if not op.exists(path):
        os.mkdir(path)
    _ix = create_in(path, schema)
    for content in contents:
        update_document(content)


def delete_document(page):
    """Delete document
    :param page: Content to delete
    """
    # create writer
    writer = _ix.writer()
    writer.delete_by_term('path', unicode(page.path))
    writer.commit()


def update_document(page):
    """Add or update a document to index

    :param page: Content to index
    """
    # create writer
    writer = _ix.writer()
    # update content
    # if path not exists it will create it
    writer.update_document(title=unicode(page.title),
                           path=unicode(page.path),
                           content=unicode(page.body))
    # commit
    writer.commit()


def search_query(query_str):
    """Search in indexed documents

    :param query_str: Query to search in indexed components
    """
    contents_result = []
    with _ix.searcher() as searcher:
        # parse query
        parser = QueryParser("content", _ix.schema)
        query = parser.parse(query_str)
        # search
        results = searcher.search(query)
        # get results
        for result in results:
            path = result['path']
            page = contents.get(path)
            if page:
                contents_result.append(page)
        return contents_result
