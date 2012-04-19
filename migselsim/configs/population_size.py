# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class PopulationSize(ConfigPlugin):
    key = 'population size'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simulator):
        PopulationSize.verifyParent(parent)
