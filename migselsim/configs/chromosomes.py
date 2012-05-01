# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class Chromosomes(ConfigPlugin):
    key = 'chromosomes'
    requirement = 'required'
    parent = None
    conflict = None

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
