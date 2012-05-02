# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin
from migselsim.definition import UNIFORM_DISTRIBUTION

class MatingScheme(ConfigPlugin):
    key = 'mating scheme'
    requirement = 'required'
    parent = 'population structure'
    conflict = None
    simple_entries = ('number of offspring per mating')

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        for item in value.iteritems():
            [key, val] = item
            if key in self.simple_entries:
                key = key.replace(' ', '_')
                self.__getattribute__(key)(val, simulator)
            else:
                self.action(key).configure(val, self.key, simulator)

    def number_of_offspring_per_mating(self, val, simulator):
        try:
            simulator.number_of_offspring = int(val)
        except TypeError:
            key = val[0]
            params = [float(i) for i in val[1:]]
            try:
                key = key.lower()
            except:
                pass
            if key == 'uniform':
                simulator.number_of_offspring = \
                    (UNIFORM_DISTRIBUTION, params[0], params[1])
            else:
                raise NotImplementedError
