# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe, NodeFactory

class root(ConfigRecipe):
    key = 'root'
    parent = None
    child = ['genetic structure', 'population structure', 'number of replicates']
    conflict = None

    @staticmethod
    def apply(cls, node, sim):
        cls.validate(node)
        for child in node.children:
            if child.id in cls.child:
                cls.apply(child, sim)
