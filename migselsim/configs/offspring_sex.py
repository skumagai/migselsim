# -*- mode: python; coding: utf-8; -*-
import math

from migselsim.configs import ConfigPlugin
from migselsim.definition import RandomMating, getRNG, UNIFORM_DISTRIBUTION, MALE, FEMALE

_tolerance = 1e-6

class OffspringSex(ConfigPlugin):
    key = 'offspring sex'
    requirement = 'required'
    parent = 'mating scheme'
    conflict = None

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        prop = float(value['proportion of male'])
        key = value['mode']
        key = key.replace(' ', '_')
        simulator.sex_mode = self.__getattribute__(key)(prop)

    def exact(self, prop):
        """Return generator function determining sex of offspring.

        The sex ratio is exactly at `prop`
        """
        if not is_almost_equal(prop, 0.5, _tolerance):
            raise NotImplementedError

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

    def by_proportion(self, prop):
        """Return generator function determining sex of offspring.

        Male offspring is exactly `prop` of all offspring.
        """




def is_almost_equal(value, target, tolr):
    if abs(value - target) < tolr:
        return True
    else:
        return False
