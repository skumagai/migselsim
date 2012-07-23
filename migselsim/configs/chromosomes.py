# -*- mode: python; coding: utf-8; -*-

from migselsim.definition import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIAL
from migselsim.configs import ConfigRecipe

class ChromosomalType(ConfigRecipe):
    key = 'chromosomes:type'

    autosomes = ['AUTOSOME', 'A', 'AUTO']
    xs = ['X', 'CHROMOSOME X']
    ys = ['Y', 'CHROMOSOME Y']
    mts = ['MT', 'MITO', 'MITOCHONDRIUM', 'MITOCHONDRIA', 'MITOCHONDRIAL']

    @classmethod
    def apply(cls, node):
        cnodes = node.get('type')
        ctypes = []
        n_cnodes = len(cnodes)
        if n_cnodes > 1:
            for cnode in cnodes:
                ctypes.append(cls.determine_type(cnode.upper()))
        elif n_cnodes == 1:
            ctypes = cls.determine_type(cnodes[0].upper())
        else:
            # default to autosome
            ctypes = AUTOSOME
        return ctypes

    @staticmethod
    def determine_type(ctype):
        cls = ChromosomalType
        if ctype in cls.autosomes:
            return AUTOSOME
        elif ctype in cls.xs:
            return CHROMOSOME_X
        elif ctype in cls.ys:
            return CHROMOSOME_Y
        elif ctype in cls.mts:
            return MITOCHONDRIAL
        else:
            raise KeyError
