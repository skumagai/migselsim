# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe

class PopulationSize(ConfigRecipe):
    """Parse and set population size of simulated population."""

    key = 'population size'
    requirement = 'required'
    parent = 'population structure'
    conflict = None

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        try:
            simulator.population_size = [int(val) for val in value]
        except TypeError:
            simulator.population_size = [int(value)]
        ndemes = len(simulator.population_size)
        simulator.subPopNames = ['deme ' + str(i) for i in range(ndemes)]
