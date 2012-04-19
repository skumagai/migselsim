# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class PositionOfNonNeutralLoci(ConfigPlugin):
    key = 'position of non-neutral loci'
    requirement = 'required'
    parent = None
    conflict = None

    def main(self, value, parent, simulator):
        PositionOfNonNeutralLoci.verifyParent(parent)
