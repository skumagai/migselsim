# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class RecombinationRate(ConfigPlugin):
    key = 'recombination rate'
    requirement = 'required'
    parent = 'chromosomes'
    conflict = None

    def configure(self, value, parent, simulator):
        RecombinationRate.verifyParent(parent)
