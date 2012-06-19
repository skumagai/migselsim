# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe
from migselsim.definition import RandomMating

class MatingType(ConfigRecipe):
    key = 'mating type'
    requirement = 'required'
    parent = 'mating scheme'
    conflict = None

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        try:
            mating_type = value.lower()
            if mating_type == 'random mating':
                simulator.mating_type = RandomMating
            else:
                raise NotImplementedError
        except AttributeError:
            raise
