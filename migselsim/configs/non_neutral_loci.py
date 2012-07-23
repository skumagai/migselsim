# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe
from migselsim.definition import ALL_AVAIL, MALE, FEMALE

class NonNeutralLoci(ConfigRecipe):
    key = 'non-neutral loci'

    @staticmethod
    def apply(node):

        return []

class InitialFrequency(ConfigRecipe):
    key = 'non-neutral loci:initial frequency'

    @classmethod
    def apply(cls, node):
        """return information of non-neutral locus.

        Initial frequency is normalized if necessary."""
        position = _get_position(node)
        chromosome = _get_chromosome(node)
        init_freq = [init for c in node.children for init in c.children
                     if init.id == 'initial frequency']
        if len(init_freq) != 1:
            # make sure there is only one 'initial frequency' per
            # single loci specificiation.
            raise Error
        else:
            # get rid of list to expose an atomic element.
            init_freq = init_freq[0]
        f = _get_list_of_values

        test_node = init_freq.children[0]
        if hasattr(test_node, 'value'):
            # no sex- and deme-specific selection
            return _build_loci_from_list(f, init_freq, chromosome, position, (ALL_AVAIL, ALL_AVAIL))
        elif test_node.id == 'male' or test_node.id == 'female':
            # sex-specific but not deme-specific
            return _build_loci_from_sex_dict(f, init_freq, chromosome, position, ALL_AVAIL)
        else:
            # either deme-specific or sex- and deme-specific.
            eid = init_freq.children[0].children[0].id
            if eid == 'male' or eid == 'female':
                # sex- and deme-specific
                return _build_loci_from_sex_dict(f, init_freq, chromosome, position)
            else:
                # deme-specific
                return _build_loci_from_list(f, init_freq, chromosome, position)


class SelectionCoefficient(ConfigRecipe):
    key = 'non-neutral loci:selection coefficient'

    @classmethod
    def apply(cls, node):
        selcoeff = [n for c in node.children for n in c.children
                    if n.id == 'selection coefficient']

        position = _get_position(node)
        chromosome = _get_chromosome(node)

        # make sure there is a single specification of selection
        # coefficient per locus.
        if len(selcoeff) != 1:
            raise Error
        else:
            selcoeff = selcoeff[0]
        f = _get_dict_of_values

        testnode = selcoeff.children[0]
        if hasattr(testnode, 'value'):
            # no sex- and deme-specific selection
            return _build_loci_from_list(f, selcoeff, chromosome, position, [(ALL_AVAIL, ALL_AVAIL)])
        elif testnode.id == 'male' or testnode.id == 'female':
            # sex-specific
            return _build_loci_from_sex_dict(f, selcoeff, chromosome, position, ALL_AVAIL)
        else:
            # either deme-sepcific or, sex- and deme-specific
            eid = testnode.children[0].id
            if eid == 'male' or eid == 'female':
                # sex- and deme-specific
                return _build_loci_from_sex_dict(f, selcoeff, chromosome, position)
            else:
                # deme-specific
                return _build_loci_from_list(f, selcoeff, chromosome, position)


def _build_loci_from_list(func, node, chrom, pos, loc=None):
    if loc is not None:
        return Locus(func(node), chrom, pos, loc)
    else:
        loci = []
        for i, d in enumerate(node.children):
            loci.append(_build_loci_from_list(func, d, chrom, pos, [(i, ALL_AVAIL)]))
        return loci


def _build_loci_from_sex_dict(func, node, chrom, pos, deme=None):
    loci = []
    if deme is not None:
        # not deme-specific
        for c in node.children:
            if c.id == 'male':
                demes = [(deme, MALE)]
            elif c.id == 'female':
                demes = [(deme, FEMALE)]
            else:
                raise Error

            loci.append(Locus(func(c), chrom, pos, demes))
        return loci
    else:
        # deme-specific
        for i, d in enumerate(node.children):
            loci.extend(_build_loci_from_sex_dict(func, d, chrom, pos, i))
        return loci

class Locus(object):
    def __init__(self, val, chrom, loci, subPops):
        self.val = val
        self.chrom = chrom
        self.loci = loci
        self.subPops = subPops


def _get_list_of_values(node):
    return [c.value for c in node.children]


def _get_dict_of_values(node):
    return {eval(c.id): c.value for c in node.children}


def _get_chromosome(node):
    return int(node.parent.id[11:])

def _get_position(node):
    pos = [pos for c in node.children for pos in c.children
           if pos.id == 'position']
    n_loci = node.parent.get('number of loci')[0]
    if len(pos) > n_loci:
        raise Error

    positions = [p.value for p in pos]

    if all([True for p in positions if 0 <= p < n_loci]):
        return positions
