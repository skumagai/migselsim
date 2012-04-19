# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class RecombinationAfterLoci(ConfigPlugin):
    key = 'recombination after loci'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simulator):
        RecombinationAfterLoci.verifyParent(parent)
