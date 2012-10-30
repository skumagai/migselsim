# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigRecipe
from migselsim.configs.utils import get_chromosome, get_values, get_position, choose_most_specific_scenario, get_scenario, build_loci
from migselsim.definition import ALL_AVAIL, MALE, FEMALE
from migselsim.definition import SCENARIO as s



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

        test_node = init_freq.children[0]
        mode = get_scenario(node, 'initial frequency')
        n_demes = len(node.root().get('population size'))
        return build_loci(init_freq, chromosome, position, mode, mode, n_demes)


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
        mode = choose_most_specific_scenario(node, 'non-neutral loci', 'selection coefficient')

        selcoeff = node.getNodes('selection coefficient')
        # make sure there is a single specification of selection
        # coefficient per locus.
        if len(selcoeff) != 1:
            raise Error
        else:
            selcoeff = selcoeff[0]

        true_mode = get_scenario(node, 'selection coefficient')
        position = get_position(node)
        # selection must be specified locus-by-locus.
        if len(position) != 1:
            raise Error
        else:
            position = position[0]
        chromosome = get_chromosome(node)

        n_demes = len(node.root().get('population size'))
        return build_loci(selcoeff, chromosome, position, mode, true_mode, n_demes)
