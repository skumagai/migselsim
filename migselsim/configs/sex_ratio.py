# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class SexRatio(ConfigPlugin):
    key = 'SexRatio'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simulator):
        SexRatio.verifyParent(parent)
