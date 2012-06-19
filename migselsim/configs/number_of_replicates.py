# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe

class NumberOfReplicates(ConfigRecipe):
    key = 'number of replicates'
    requirment = 'required'
    parent = None
    conflict = None

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        simulator.number_of_replicates = int(value)
