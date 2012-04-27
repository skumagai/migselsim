# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin
from migselsim.core import RandomMating, getRNG, UNIFORM_DISTRIBUTION, MALE, FEMALE

class OffspringSex(ConfigPlugin):
    key = 'offsprint sex'
    requirement = 'required'
    parent = 'mating scheme'
    conflict = None
    simple_entries = ('exact', 'by probability')

    def configure(self, value, parent, simulator):
        OffspringSex.verifyParent(parent)
        if 'exact' in value and 'by probability' in value:
            # should use different exception.
            raise TypeError
        elif 'exact' in value:
            simulator.sex_mode = self.exact(float(value['proportion']))
        elif 'by probability':
            simulator.sex_mode = (PROB_OF_MALES, float(value['proportion']))
        else:
            raise NotImplementedError

    def exact(self, prop):
        """Return generator function determining sex of offspring.

        The sex ratio is exactly at `prop`
        """
        def mating_func():
            current = MALE
            while True:
                if current == MALE:
                    current = FEMALE
                else:
                    current = MALE
                yield current

        return mating_func

    def by_probability(self, prop):
        """Return generator function determining sex of offspring.

        Offspring is male `prop` of time, and female 1 - `prop` of time.
        """
        def mating_func():
            rng = getRNG()
            while True:
                sex = MALE
                if rng.randUniform() > prop:
                    sex = FEMALE
                yield sex
        return mating_func
