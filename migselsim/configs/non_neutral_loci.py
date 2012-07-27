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
            return build_loci_from_list(f, init_freq, chromosome, position, [(ALL_AVAIL, ALL_AVAIL)])
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
        # when combine selection on multiple loci using MlSelector in
        # simuPOP, the class only works if every (Map/Ma)Selectors
        # have identical target population (sex and demes).
        #
        # This means that mulitple single locus selectors may be
        # provided even if a mode of selection on the particular locus
        # is neither sex- nor deme-specific.
        #
        # Do test what's the most general case upfront.
        mode = cls.most_specific_scenario(node)

        selcoeff = [n for c in node.children for n in c.children
                    if n.id == 'selection coefficient']

        position = get_position(node)
        # selection must be specified locus-by-locus.
        if len(position) != 1:
            raise Error
        else:
            position = position[0]
        chromosome = get_chromosome(node)

        # make sure there is a single specification of selection
        # coefficient per locus.
        if len(selcoeff) != 1:
            raise Error
        else:
            selcoeff = selcoeff[0]
        f = get_dict_of_values

        testnode = selcoeff.children[0]
        if mode == 'not specific':
            # no sex- and deme-specific selection
            #
            # if mode is 0, it means that I don't need to do any
            # special thing to get right.
            return build_loci_from_list(f, selcoeff, chromosome, position,
                                        [(ALL_AVAIL, ALL_AVAIL)])

        elif mode == 'deme specific':
            # like when mode is 1, I must use special path in case a
            # locus is neither sex- nor deme-specific.
            # if hasattr(testnode.children[0], 'value'):
            if not hasattr(testnode, 'value'):
                return build_loci_from_list(f, selcoeff, chromosome, position)
            else:
                # special path for non deme-specific locus.
                n_demes = len(node.root().get('population size'))
                return [build_loci_from_list(f, selcoeff, chromosome, position,
                                             [(i, ALL_AVAIL)])
                        for i in range(n_demes)]

        elif mode == 'sex specific':
            # if mode is 1, I must use special path in case a locus is
            # actually neither sex- nor deme-specific.
            if testnode.id == 'male' or testnode.id == 'female':
                # sex-specific
                return build_loci_from_sex_dict(f, selcoeff, chromosome, position, ALL_AVAIL)
            else:
                # actually not sex-specific, but required to do this
                # for the sake of other loci.
                return [build_loci_from_list(f, selcoeff, chromosome, position,
                                             [(ALL_AVAIL, i)])
                        for i in [MALE, FEMALE]]

        else:
            # sex- and deme-specific

            # here, at last I need all the special path because an
            # acutal locus can be any of four possible states.

            # either deme-sepcific or, sex- and deme-specific
            if hasattr(testnode, 'value'):
                # true mode 0
                n_demes = len(node.root().get('population size'))
                return [build_loci_from_list(f, selcoeff, chromosome, position, [(i, j)])
                        for i in range(n_demes) for j in [MALE, FEMALE]]

            elif testnode.id == 'male' or testnode.id == 'female':
                # true mode 2
                n_demes = len(node.root().get('population size'))
                return [build_loci_from_sex_dict(f, selcoeff, chromosome, position, i)
                        for i in range(n_demes)]
            else:
                eid = testnode.children[0].id
                if eid == 'male' or eid == 'female':
                    # true mode 4
                    return build_loci_from_sex_dict(f, selcoeff, chromosome, position)
                else:
                    # true mode 1
                    return [build_loci_from_list(f, c, chromosome, position, [(i, j)])
                            for i, c in enumerate(selcoeff.children) for j in [MALE, FEMALE]]


    @staticmethod
    def most_specific_scenario(node):
        non_neuts = [n for n in node.root().descendents()
                     if n.id == 'non-neutral loci']
        mode = []

        for n in non_neuts:
            sel = n._getNode('selection coefficient', n.descendents())
            if sel is None:
                raise Error
            test_node = sel.children[0]
            if hasattr(test_node, 'value'):
                mode.append(0)
            elif test_node.id == 'male' or test_node.id == 'female':
                mode.append(1)
            else:
                if hasattr(test_node.children[0], 'value'):
                    mode.append(2)
                else:
                    mode.append(3)

        if max(mode) == 0:
            return 'not specific'
        elif max(mode) == 1:
            return 'sex specific'
        elif max(mode) == 2:
            if 1 not in mode:
                return 'deme specific'
            else:
                return 'sex and deme specific'
        else:
            return 'sex and deme specific'
