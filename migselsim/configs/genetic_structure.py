# -*- mode: python; coding: utf-8; -*-

"""Set genetic structure of simulated indiviudals.

Simple settings are handles are directly handled by this, but more complex
settings are delegated to specialized plugins.
"""

from migselsim.configs import ConfigPlugin
from migselsim.definition import HAPLODIPLOID
from migselsim.exception import InvalidConfigValueError

class GeneticStructure(ConfigPlugin):
    key = 'genetic structure'
    requirement = 'required'
    parent = None
    conflict = None

    simple_keys = ('ploidy')

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)

        for key in value:
            lkey = key.lower()
            lkey = lkey.replace(' ', '_')
            if lkey in self.simple_keys:
                self.__getattribute__(lkey)(value[key], simulator)
            else:
                self.action(key).configure(value[key], self.key, simulator)


    def ploidy(self, value, simulator):
        try:
            ploidy = value.lower()
            if ploidy == 'haplodiploid':
                simulator.ploidy = HAPLODIPLOID
            else:
                raise InvalidConfigValueError('ploidy', value, 'Invalid value')
        except :
            simulator.ploidy = value
