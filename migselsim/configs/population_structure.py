# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class PopulationStructure(ConfigPlugin):
    key = 'population structure'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simlator):
        PopulationStructure.verifyParent(parent)
