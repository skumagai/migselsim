# -*- mode: python; coding: utf-8; -*-

import re

from migselsim.definition import MALE, FEMALE, ALL_AVAIL
from migselsim.definition import SCENARIO as s

class Locus(object):
    def __init__(self, val, chrom, loci, subPops):
        self.val = val
        self.chrom = chrom
        self.loci = loci
        self.subPops = subPops


def get_list_of_values(node):
    if len(node.children) == 0 and hasattr(node, 'value'):
        return [node.value]
    else:
        # default mode of action
        return [c.value for c in node.children]


def get_dict_of_values(node):
    return {eval(c.id): c.value for c in node.children}


def get_chromosome(node):
    n = node
    pattern = 'chromosomes\d+'
    hit = re.search(pattern, n.id)
    while n.parent is not None and hit is None:
        n = n.parent
        hit = re.search(pattern, n.id)

    if n is not None:
        return n.parent.children.index(n)
    else:
        raise Error

def get_position(node):
    pos = [pos for c in node.children for pos in c.children
           if pos.id == 'position']
    n_loci = node.parent.get('number of loci')[0]
    if len(pos) > n_loci:
        raise Error

    positions = [p.value for p in pos]

    if all([True for p in positions if 0 <= p < n_loci]):
        return positions


def build_loci_from_list(func, node, chrom, pos, loc=None):
    if loc is not None:
        return [Locus(func(node), chrom, pos, loc)]
    else:
        loci = []
        for i, d in enumerate(node.children):
            loci.append(build_loci_from_list(func, d, chrom, pos, [(i, ALL_AVAIL)]))
        return loci


def build_loci_from_sex_dict(func, node, chrom, pos, deme=None):
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
            loci.extend(build_loci_from_sex_dict(func, d, chrom, pos, i))
        return loci

def choose_most_specific_scenario(node, key1, key2):
    nodes = node.root().getNodes(key1)

    mode = set([get_scenario(n, key2) for n in nodes])

    n_mode = len(mode)
    if n_mode == 1 and s.NOT_SPECIFIC in mode:
        return s.NOT_SPECIFIC
    elif (n_mode == 1 and s.SEX_SPECIFIC in mode) or \
            (n_mode == 2 and s.NOT_SPECIFIC in mode and s.SEX_SPECIFIC in mode):
        return s.SEX_SPECIFIC
    elif (n_mode == 1 and s.DEME_SPECIFIC in mode) or \
            (n_mode == 2 and s.NOT_SPECIFIC in mode and s.DEME_SPECIFIC in mode):
        return s.DEME_SPECIFIC
    else:
        return s.SEX_AND_DEME_SPECIFIC


def get_scenario(node, key):
    nodes = node.getNodes(key)
    if len(nodes) == 1:
        n = nodes[0]
    else:
        raise Error

    test_node = n.children[0]
    if hasattr(test_node, 'value'):
        return s.NOT_SPECIFIC
    elif test_node.id == 'male' or test_node.id == 'female':
        return s.SEX_SPECIFIC
    else:
        if hasattr(test_node.children[0], 'value'):
            return s.DEME_SPECIFIC
        else:
            return s.SEX_AND_DEME_SPECIFIC

def build_loci(f, val, chrom, pos, mode, true_mode, n_demes):

    if mode is s.NOT_SPECIFIC:
        # no sex- and deme-specific selection
        #
        # if mode is 0, it means that I don't need to do any
        # special thing to get right.
        return build_loci_from_list(f, val, chrom, pos,
                                    [(ALL_AVAIL, ALL_AVAIL)])

    elif mode is s.SEX_SPECIFIC and true_mode is s.NOT_SPECIFIC:
        return [build_loci_from_list(f, val, chrom, pos,
                                     [(ALL_AVAIL, i)])
                for i in [MALE, FEMALE]]

    elif mode is s.SEX_SPECIFIC:
        # if mode is 1, I must use special path in case a locus is
        # actually neither sex- nor deme-specific.
        return build_loci_from_sex_dict(f, val, chrom, pos, ALL_AVAIL)

    elif mode is s.DEME_SPECIFIC and true_mode is s.NOT_SPECIFIC:
        return [build_loci_from_list(f, val, chrom, pos,
                                     [(i, ALL_AVAIL)])
                for i in range(n_demes)]

    elif mode is s.DEME_SPECIFIC:
        return build_loci_from_list(f, val, chrom, pos)

    elif mode is s.SEX_AND_DEME_SPECIFIC and true_mode is s.NOT_SPECIFIC:
        return [build_loci_from_list(f, val, chrom, pos, [(i, j)])
                for i in range(n_demes) for j in [MALE, FEMALE]]

    elif mode is s.SEX_AND_DEME_SPECIFIC and true_mode is s.SEX_SPECIFIC:
        return [build_loci_from_sex_dict(f, val, chrom, pos, i)
                for i in range(n_demes)]

    elif mode is s.SEX_AND_DEME_SPECIFIC and true_mode is s.DEME_SPECIFIC:
        return [build_loci_from_list(f, c, chrom, pos, [(i, j)])
                for i, c in enumerate(val.children) for j in [MALE, FEMALE]]

    else:
        return build_loci_from_sex_dict(f, val, chrom, pos)
