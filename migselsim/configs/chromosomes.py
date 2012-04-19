# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class Chromosomes(ConfigPlugin):
    key = 'chromosomes'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simulator):
        Chromosomes.verifyParent(parent)
