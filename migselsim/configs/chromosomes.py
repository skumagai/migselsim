# -*- mode: python; coding: utf-8; -*-

from migselsim.definition import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIAL, ALL_AVAIL, MALE, FEMALE
from migselsim.definition import SCENARIO as s
from migselsim.configs import ConfigRecipe
from migselsim.configs.utils import get_chromosome, get_position, get_list_of_values, choose_most_specific_scenario, get_scenario, build_loci, Locus

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

class Recombination(ConfigRecipe):

    key = 'chromosomes:recombination'

    @classmethod
    def apply(cls, node):

        scenario = choose_most_specific_scenario(node, 'recombination', 'rate')

        recs = node.getNodes('recombination')
        loci = []
        f = get_list_of_values
        # f = lambda x: x
        n_demes = len(node.root().get('population size'))
        for r in recs:
            chromosome = get_chromosome(r)
            pos = get_list_of_values(r.descendent('at'))
            n_pos = len(pos)
            true_scenario = get_scenario(r, 'rate')

            rate = r.getNodes('rate')
            if len(rate) != 1:
                raise Error
            else:
                rate = rate[0]
            loci.extend(build_loci(f, rate, chromosome, pos, scenario, true_scenario, n_demes))

        new_loci = []
        for l in loci:
            new_loci.extend([Locus(v, l.chrom, p, l.subPops)
                             for v, p in zip(l.val, l.loci)])


        return new_loci

    @staticmethod
    def set_rate(node, chrom, pos, loc):
        rate = get_list_of_values(node)
        if len(rate) == 1 or len(rate) == len(pos):
            return Locus(rate, chrom, pos, loc)
        else:
            raise Error
