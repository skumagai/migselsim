# -*- mode: python; coding: utf-8; -*-

# geno_initiator.py - brief description

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
from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA

class InitGenotype(sim.PyOperator):
    """Set genotypes of members of an original population.

    This assigns IDs to alleles in neutral loci, and also set
    incompatibility  loci to locally adapted alleles.

    IDs are assigned to all alleles at all neutral loci.  Within
    each locus, no two chromosome shares an identical ID.  This
    allows to check coalescence later.

    Assignment of locally adapted alleles at incompatibility factors
    are performed deme-by-deme basis so that all individuals are
    locally adapted in each deme.

    In deme 0, all individuals have "0" allele, which is locally
    adapted, at every incompatibility factor loci, and they all
    have "1" allele in deme 1, which is equally adapted in deme 1.
    """

    def __init__(self,
                 markers = [0] * 4,
                 factors = [],
                 chromTypes = [AUTOSOME,
                               CHROMOSOME_X,
                               CHROMOSOME_Y,
                               MITOCHONDRIA],
                 mutation=False,
                 *args, **kwargs):
        """Set up genotype initializer.

        Arguments:
        markers: a list of neutral markers (default [0, 0, 0, 0])
        factors: a list of factors (default no factor ([]))
        chromTypes: type of chromosomes, on which markers are located
        *args, **kwargs: pass to PyOperator.
        """
        self._markers = markers
        self._factors = factors
        self._chromTypes = chromTypes
        self._mutation = mutation
        sim.PyOperator.__init__(self, func = self.setGenotype,
                                *args, **kwargs)

    def setGenotype(self, pop):
        """Set genotype of all individuals.

        Arguments:
        pop: population object
        """

        pop_size = pop.popSize()
        markers = self._markers
        chromTypes = self._chromTypes
        factors = self._factors

        num_chroms = pop.numChrom()

        # Tagging alleles
        for marker, chrom  in zip(markers, chromTypes):
            count = 0
            if chrom == AUTOSOME:
                for ind in pop.individuals():
                    for p in [0, 1]:
                        ind.setAllele(count, marker,
                                      ploidy = p, chrom = chrom)
                        count += 1
            elif chrom == CHROMOSOME_X:
                for ind in pop.individuals():
                    if ind.sex() == sim.MALE:
                        ind.setAllele(count, marker,
                                      ploidy = 0, chrom = chrom)
                        count += 1
                    else:
                        for p in [0, 1]:
                            ind.setAllele(count, marker,
                                          ploidy = p, chrom = chrom)
                            count += 1
            elif chrom == CHROMOSOME_Y:
                for ind in pop.individuals():
                    if ind.sex() == sim.MALE:
                        ind.setAllele(count, marker,
                                      ploidy = 1, chrom = chrom)
                        count += 1
            else:
                for ind in pop.individuals():
                    ind.setAllele(count, marker,
                                  ploidy = 0, chrom = chrom)
                    count += 1

        # for i, ind in enumerate(pop.individuals()):
        #     for j in range(num_chroms):
        #         marker = markers[j]
        #         ind.setAllele(2 * i, marker,
        #                       ploidy = 0, chrom = j)
        #         ind.setAllele(2 * i + 1, marker,
        #                       ploidy = 1, chrom = j)



        # Setting up incompatibility factors
        if factors is not None:
            if self.mutation is True:
                locus = 2
            else:
                locus = 1
            for f in factors:
                for d in range(pop.numSubPop()):
                    for i in pop.individuals(subPop = d):
                        for p in range(2):
                            i.setAllele(d, locus, ploidy = p, chrom = f)
        return True

