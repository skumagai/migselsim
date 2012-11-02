# -*- mode: python; coding: utf-8; -*-

from lxml import etree

class XML(object):
    def __init__(self, fh):
        self.data = etree.parse(fh)

    def get(self, key):
        pass
