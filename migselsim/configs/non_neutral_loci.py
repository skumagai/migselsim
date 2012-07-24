# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe
from migselsim.configs.utils import get_chromosome, get_position, get_list_of_values, get_dict_of_values, Locus, build_loci_from_list, build_loci_from_sex_dict
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
        position = get_position(node)
        chromosome = get_chromosome(node)
        init_freq = [init for c in node.children for init in c.children
                     if init.id == 'initial frequency']
        if len(init_freq) != 1:
            # make sure there is only one 'initial frequency' per
            # single loci specificiation.
            raise Error
        else:
            # get rid of list to expose an atomic element.
            init_freq = init_freq[0]
        f = get_list_of_values

        test_node = init_freq.children[0]
        if hasattr(test_node, 'value'):
            # no sex- and deme-specific selection
            return build_loci_from_list(f, init_freq, chromosome, position, (ALL_AVAIL, ALL_AVAIL))
        elif test_node.id == 'male' or test_node.id == 'female':
            # sex-specific but not deme-specific
            return build_loci_from_sex_dict(f, init_freq, chromosome, position, ALL_AVAIL)
        else:
            # either deme-specific or sex- and deme-specific.
            eid = init_freq.children[0].children[0].id
            if eid == 'male' or eid == 'female':
                # sex- and deme-specific
                return build_loci_from_sex_dict(f, init_freq, chromosome, position)
            else:
                # deme-specific
                return build_loci_from_list(f, init_freq, chromosome, position)


class SelectionCoefficient(ConfigRecipe):
    key = 'non-neutral loci:selection coefficient'

    @classmethod
    def apply(cls, node):
        selcoeff = [n for c in node.children for n in c.children
                    if n.id == 'selection coefficient']

        position = get_position(node)
        chromosome = get_chromosome(node)

        # make sure there is a single specification of selection
        # coefficient per locus.
        if len(selcoeff) != 1:
            raise Error
        else:
            selcoeff = selcoeff[0]
        f = get_dict_of_values

        testnode = selcoeff.children[0]
        if hasattr(testnode, 'value'):
            # no sex- and deme-specific selection
            return build_loci_from_list(f, selcoeff, chromosome, position, [(ALL_AVAIL, ALL_AVAIL)])
        elif testnode.id == 'male' or testnode.id == 'female':
            # sex-specific
            return build_loci_from_sex_dict(f, selcoeff, chromosome, position, ALL_AVAIL)
        else:
            # either deme-sepcific or, sex- and deme-specific
            eid = testnode.children[0].id
            if eid == 'male' or eid == 'female':
                # sex- and deme-specific
                return build_loci_from_sex_dict(f, selcoeff, chromosome, position)
            else:
                # deme-specific
                return build_loci_from_list(f, selcoeff, chromosome, position)
