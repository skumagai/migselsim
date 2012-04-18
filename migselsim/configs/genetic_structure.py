# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class GeneticStructure(ConfigPlugin):
    key = 'genetic structure'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent):
        pass
