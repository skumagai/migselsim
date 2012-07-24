# -*- mode: python; coding: utf-8; -*-

from migselsim.definition import MALE, FEMALE, ALL_AVAIL

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
    return int(node.parent.id[11:])

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
        return Locus(func(node), chrom, pos, loc)
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
