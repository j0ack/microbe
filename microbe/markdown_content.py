#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Markdown for Microbe app
"""

from markdown import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

__author__ = u'TROUVERIE Joachim'


class CenterAlignPattern(Pattern):
    """Pattern to center elements"""
    def handleMatch(self, m):
        div = etree.Element('div')
        div.set('style', 'display:block;text-align:center;')
        div.text = m.group(3)
        return div


class RightAlignPattern(Pattern):
    """Pattern to right elements"""
    def handleMatch(self, m):
        div = etree.Element('div')
        div.set('style', 'display:block;text-align:right;')
        div.text = m.group(3)
        return div


class AlignExtension(Extension):
    """Align extension for Markdown

        Center or align to right elements
        -> center element <-
        -> align to right element ->
    """
    def extendMarkdown(self, md, md_globals):
        CENTR_RE = r'(\-\>)(.+?)(\<\-)'
        RIGHT_RE = r'(\-\>)(.+?)(\-\>)'
        center_pattern = CenterAlignPattern(CENTR_RE)
        right_pattern = RightAlignPattern(RIGHT_RE)
        md.inlinePatterns.add('CenterAlign', center_pattern, "<not_strong")
        md.inlinePatterns.add('RightAlign', right_pattern, "<not_strong")


def render_markdown(content):
    """Translate markdown to HTML

    :param content: markdown content
    """
    return markdown(content, extensions=['codehilite', 'tables',
                                         AlignExtension()])
