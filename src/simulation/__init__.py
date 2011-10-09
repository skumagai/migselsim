# -*- mode: python; coding: utf-8; -*-

# __init__.py - brief description

# Copyright (C) 2011 Seiji Kumagai <seiji.kumagai@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import simuPOP as sim
import mutation as mut

# Use global variable to carry over history of mutation and maximum
# allele states.  These information are necessary to convert from the
# infinite allele model, in which simulations are performed, to the
# infinite site model.

# I cannot find a way to access history without using global...

## Global variables

# Mutation space (history of mutation and number of alleles so far)
mutation = mut.Mutation()

# Genealogy
genealogies = []

# Global constants

# Set of Standard chromosomes
AUTOSOME = 0
CHROMOSOME_X = 1
CHROMOSOME_Y = 2
MITOCHONDRIA = 3

# Utility functions

def get_genes(pop, chrom, locus = 1):
    """Construct a list of genes for entire population.

    Genes are ordered by individual-by-indivudal.  The first half of
    the list holds genes from deme 1 and the second half from deme 2.

    Arguments:
    pop: Population object
    chrom: chromosome, on which a locus is located.
    locus: index of locus (within a chromosome)
    """

    # Iterate over subpopulation to make sure that genes from the first
    # deme is stored before genes from the second deme.

    if chrom == AUTOSOME:
        genes = [ind.allele(locus, ploidy = j, chrom = chrom)
                 for deme in range(2)
                 for ind in pop.individuals(subPop = [deme])
                 for j in range(2)]
    elif chrom == CHROMOSOME_X:
        genes = [ind.allele(locus, ploidy = j, chrom = chrom)
                 for deme in range(2)
                 for ind in pop.individuals(subPop = [deme])
                 for j in range(2)
                 if ind.sex() == sim.FEMALE or j == 0]
    elif chrom == CHROMOSOME_Y:
        genes = [ind.allele(locus, ploidy = 1, chrom = chrom)
                 for deme in range(2)
                 for ind in pop.individuals(subPop = [deme])
                 if ind.sex() == sim.MALE]
    elif chrom == MITOCHONDRIA:
        genes = [ind.allele(locus, ploidy = 0, chrom = chrom)
                 for deme in range(2)
                 for ind in pop.individuals(subPop = [deme])]
    return genes



def rename_alleles(pop, chrom, name_map):
    """Rename alleles of Individual object to reflex the pruning process.

    Arguments:
    pop: Population object
    chrom: chromosome, on which a locus is located
    name_map: dict of old names to new names
    """
    if chrom == AUTOSOME:
        for ind in pop.individuals():
            for ploidy in range(2):
                old = ind.allele(1, ploidy = ploidy, chrom = chrom)
                ind.setAllele(name_map[old], 1,
                              ploidy = ploidy, chrom = chrom)
    if chrom == CHROMOSOME_X:
        for ind in pop.individuals():
            old = ind.allele(1, ploidy = 0, chrom = chrom)
            ind.setAllele(name_map[old], 1, ploidy = 0, chrom = chrom)
            if ind.sex() == sim.FEMALE:
                old = ind.allele(1, ploidy = 1, chrom = chrom)
                ind.setAllele(name_map[old], 1, ploidy = 1, chrom = chrom)
    if chrom == CHROMOSOME_Y:
        for ind in pop.individuals():
            if ind.sex() == sim.MALE:
                old = ind.allele(1, ploidy = 1, chrom = chrom)
                ind.setAllele(name_map[old], 1, ploidy = 1, chrom = chrom)
    if chrom == MITOCHONDRIA:
        for ind in pop.individuals():
            old = ind.allele(1, ploidy = 0, chrom = chrom)
            ind.setAllele(name_map[old], 1, ploidy = 0, chrom = chrom)
