# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class PopulationSize(ConfigPlugin):
    """Parse and set population size of simulated population."""

    key = 'population size'
    requirement = 'required'
    parent = 'population structure'
    conflict = None

    def main(self, value, parent, simulator):
        PopulationSize.verifyParent(parent)
        try:
            simulator.population_size = [int(val) for val in value]
        except TypeError:
            simulator.population_size = [int(value)]
        simulator.number_of_demes = len(simulator.population_size)
