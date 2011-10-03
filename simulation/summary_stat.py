# -*- mode: python; coding: utf-8; -*-

# stat.py - stat clasees

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
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA
from exception import SizeError

class Fst(object):
    """Compute Fst based on Weir"""

    @classmethod
    def get(cls, genes, mutation, pop_sizes, chrom):
        """Compute Fst

        Arguments:
        genes: samples taken from population.
        mutation: object of class Mutation
        chrom: index of chromosome
        """

        history = mutation.history(chrom)

        # Number of genes in each deme.  This depends on the location
        # of loci.
        # gene_sizes = [sum([val for val in c.values()])
        #               for c in counts_part]
        if chrom == AUTOSOME:
            gene_sizes = [2 * sum(deme)
                          for deme in pop_sizes]
        elif chrom == CHROMOSOME_X:
            gene_sizes = [deme[0] + 2 * deme[1]
                          for deme in pop_sizes]
        elif chrom == CHROMOSOME_Y:
            gene_sizes = [deme[0] for deme in pop_sizes]
        else:
            gene_sizes = [sum(deme) for deme in pop_sizes]

        if sum(gene_sizes) != len(genes):
            raise SizeError(sum(gene_sizes), len(genes))

        genes_part = [genes[:gene_sizes[0]], genes[gene_sizes[0]:]]

        # Count numbers of samples having each type of alleles in each
        # deme.
        counts_part = [dict((key, g.count(key))
                            for key in history.keys()
                            if g.count(key) > 0)
                       for g in genes_part]



        len_history = len(history)
        # At this point, it is guranteed that only histories about
        # extant alleles are stored.
        if len_history == 1:
            # If population is monomorphic, Fst is undefined.
            return float('nan')

        # Compute number of differences between any pair of alleles.
        dist = mutation.pairwiseDistance(chrom)

        # Compute denominator for average pairwise distance within a
        # deme.
        denom_within = sum([(p * p - p) / 2 for p in gene_sizes])
        # Compute denominator for average pairwise distance between
        # demes.
        denom_between = gene_sizes[0] * gene_sizes[1]


        # Compute the average pairwise evolutionary distance within
        # each deme.
        h_within = measure_variation_within(dist,
                                            counts_part,
                                            denom_within)

        # Compute the average pairwise evolutionary distance between
        # two demes.
        h_between = measure_variation_between(dist,
                                              counts_part,
                                              denom_between)
        if h_between == 0.0:
            # If denominator is 0, Fst is undefinied.
            fst = float('nan')
        else:
            fst = 1.0 - h_within / h_between

        return fst


def measure_variation_within(dist, counts, denom):
    """Comupte average pairwise distance of two sequences within a deme.

    Arguments:
    dist: dictionary of distances between two sequences
    counts: list of list holding number of times particular allele appear in a population
    denom: denominator
    """
    value = 0
    for pair, d in dist.items():
        for c in counts:
            if pair[0] in c and pair[1] in c:
                value += c[pair[0]] * c[pair[1]] * d
    return float(value) / float(denom)

def measure_variation_between(dist, counts, denom):
    """Compute average pairwise distance of two sequences between demes.

    Arguments:
    dist: dictionary of distances between two sequences
    counts: list of list holding number of times particular allele appear in a population
    denom: denominator
    """
    value = 0

    for pair, d in dist.items():
        if pair[0] in counts[0] and pair[1] in counts[1]:
            value += counts[0][pair[0]] * counts[1][pair[1]] * d
        if pair[1] in counts[0] and pair[0] in counts[1]:
            value += counts[0][pair[1]] * counts[1][pair[0]] * d
    return float(value) / float(denom)

