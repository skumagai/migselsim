# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe

class RecombinationRate(ConfigRecipe):
    key = 'recombination rate'
    requirement = 'required'
    parent = 'chromosomes'
    conflict = None

    def configure(self, value, parent, simulator):
        RecombinationRate.verifyParent(parent)
