# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin
from migselsim.definition import RandomMating

class MatingType(ConfigPlugin):
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
