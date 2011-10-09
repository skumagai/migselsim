# -*- mode: python; coding: utf-8; -*-

# dumper.py - brief description

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

from .. import get_genes, rename_alleles, mutation
from ..summary_stat import Fst

class Dumper(sim.PyOperator):
    """Compute and output Fst for neutral loci.

    Fst are calculated when one of four neutral marker loci newly
    reaches a state, in which all member of current generation
    ultimately descended from a single gene in the original generation.
    """

    def __init__(self, sample_size, *args, **kwargs):
        self._sample_size = sample_size
        self.clear()
        sim.PyOperator.__init__(self, func = self.dump, *args, **kwargs)

    def clear(self):
        """Eliminate internal information associating with a run."""
        # Indicating if all members of a current generation descendent
        # a marker from a single copy.
        # False indicates segregating state.
        # True value indicates fixed state.
        self._fixation_flags = [False] * 4

        # Store genrations when a marker is first fixed.  Negative
        # value is used to indicate fixation has not been achieved at
        # a marker.
        self._fixed_generation = [-1] * 4

    def dump(self, pop):
        """Compute and output Fst.

        Arguments:
        pop: Population object.
        """
        # global fixation_flags, fixed_generation

        # Identify which neutral loci are yet to descended from MRCA.
        segregating = [i for i in range(4) if not self._fixation_flags[i]]

        need_output = []
        for chrom in segregating:
            if self.isFixed(pop, chrom):
                self._fixation_flags[chrom] = True
                self._fixed_generation[chrom] = pop.vars()['gen']
                need_output.append(str(chrom))

        if need_output:
            global mutation
            # clean up mutation space.
            for chrom in range(4):
                genes = get_genes(pop, chrom)

                # Get rid of mutation history regarding to extinct
                # alleles.
                name_map = mutation.prune(chrom, genes)
                rename_alleles(pop, chrom, name_map)

            # Compute Fsts.
            genes = [get_genes(pop, chrom) for chrom in range(4)]
            pop_sizes = [(pop.subPopSize(subPop = (deme, 0)), # Male
                          pop.subPopSize(subPop = (deme, 1))) # Female
                         for deme in range(2)]
            fsts = [Fst.get(genes[chrom], mutation,
                            pop_sizes[chrom], chrom)
                    for chrom in range(4)]
            # Output Fst with generation to STDOUT.
            print("{},{},{},{},{},{}".format(pop.vars()['gen'],
                                             ';'.join(need_output),
                                             fsts[0],
                                             fsts[1],
                                             fsts[2],
                                             fsts[3]))
            for chrom in range(4):
                # The raw data -- these can be used to do additional
                # analysis after finishing simulations.
                print(genes[chrom])
                print(mutation.numAlleles(chrom))
                print(mutation.history(chrom))

            if len([i for i in self._fixation_flags if i]) != 4:
                # Keep running a simulation if not all four marker
                # loci has a MRCA.
                return True
            else:
                # If MRCA is reached in all loci, terminate the
                # current run.

                # Reset all global variables to original states.
                # global current_max_allele, history
                # current_max_allele = [0] * 4
                # history = [{0:[None]}] * 4
                mutation.clear()
                self.clear()
                # When this function returns False, a run gets
                # terminated.
                return False
        else:
            return True

    def isFixed(self, pop, chrom):
        """Check if all sampled genes at a neutral marker locus is descended from MRCA.

        Arguments:
        pop: Population object
        chrom: chromosome, on which the neutral locus is located.
        """
        inds = pop.individuals()

        # Use the first allele in a population as a reference.
        genes = get_genes(pop, chrom, 0)
        if len(set(genes)) > 1:
            return False
        else:
            return True
