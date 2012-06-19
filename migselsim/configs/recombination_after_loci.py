# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe

class RecombinationAfterLoci(ConfigRecipe):
    key = 'recombination after loci'
    requirement = 'required'
    parent = 'chromosomes'
    conflict = None

    def configure(self, value, parent, simulator):
        RecombinationAfterLoci.verifyParent(parent)
