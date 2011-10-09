# -*- mode: python; coding: utf-8; -*-

# mutator.py - brief description

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

from .. import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA
from .. import get_genes, mutation

class InfiniteAlleleMutator(sim.PyOperator):
    """Set up and configure scheme of mutation under the infinite allele model.

    Mutations are simulated under the infinite allele model.
    When a new mutation is arisen in a population, a new allele is
    not observed in the population before.  Therefore, each mutation
    is identifiable.
    """

    def __init__(self, rate, *args, **kwargs):
        """Initialize Mutator object.

        Arguments:
        rate: mutation rates.  All loci share the same rate.
        *args, **kwargs: pass to PyOperator.
        """

        self._rate = rate
        self._unif = sim.getRNG().randUniform
        sim.PyOperator.__init__(self, func = self.mutate, *args, **kwargs)

    def setMutation(self, ind, ploidy, chrom):
        """Determines if a new mutation arises.

        Arguments:
        ind: Individual object.
        ploidy:  Which chromosome an occurrence of mutation is tested.
        chrom: Which locus an occurrence of mutation is tested.
        """

        # global current_max_allele, history
        global mutation
        if  self._unif() < self._rate:
        # if sim.getRNG().randUniform() < self._rate:
            # Get the stae of current parental allele.
            curr_allele = ind.allele(1, ploidy = ploidy, chrom = chrom)
            new_allele = mutation.addAllele(chrom, curr_allele)

            # # Get the state of new allele.
            # # current_max_allele[chrom] += 1
            # # allele = current_max_allele[chrom]


            # # Record the current allele as a parent of new allele by
            # # first making a clone of evolutionary history of the
            # # parental allele and then appending the parental allele
            # # at the end of clone.
            # # Cloning is done to make two history not sharing the same
            # # list.  Although this increases memory footprint, it is
            # # necessary so that pruning extinct allele from memory
            # # later does not affect exant alleles.
            # history[chrom][allele] = list(history[chrom][curr_allele])
            # history[chrom][allele].append(curr_allele)

            # Change the state of gene to new allele.
            ind.setAllele(new_allele, 1, ploidy = ploidy, chrom = chrom)

            # Increase the counts of allele types by one.

    def mutate(self, pop):
        """Perform test of a new mutation.

        Arguments:
        pop: Population object.
        """
        global history

        for ind in pop.individuals():
            sex = ind.sex()

            # Autosome
            for i in range(2):
                self.setMutation(ind, i, AUTOSOME)

            # Chromosome X
            self.setMutation(ind, 0, CHROMOSOME_X)
            # A new mutation in males on the 2nd of the pair of
            # chromosomes does not matter, as genes on the chromosome
            # are dummies.
            if sex == sim.FEMALE:
                self.setMutation(ind, 1, CHROMOSOME_X)

            # Mitochondria
            # Similar to chromosome X, only mutations occurred in
            # females get transmitted to offspring.
            self.setMutation(ind, 0, MITOCHONDRIA)

            # Chromosome Y
            if sex == sim.MALE:
                self.setMutation(ind, 1, CHROMOSOME_Y)

        return True

