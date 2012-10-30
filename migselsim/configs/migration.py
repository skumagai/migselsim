# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe
from migselsim.configs.utils import get_values

class MigrationMatrix(ConfigRecipe):
    key = 'migration:matrix'

    class Matrix(object):
        """simple class preventing flattening of matrix into vector."""
        def __init__(self, val):
            self.val = val

    @classmethod
    def apply(cls, node):
        mnode = node.descendent('matrix')
        dim = len(mnode.children)
        mat = []
        for row in mnode.children:
            mat.append( get_values(row))

        return cls.Matrix(mat)
