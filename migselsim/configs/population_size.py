# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe

class PopulationSize(ConfigRecipe):
    key = 'population size'
    parent = 'population structure'
    conflict = None

    @staticmethod
    def apply(node):
        PopulationSize.validate(node)
        return [pop.value for pop in node.children]
