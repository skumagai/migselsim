# -*- mode: python; coding: utf-8; -*-

# mutation_cleaner.py - brief description

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

from .. import get_genes, rename_alleles
from .. import mutation


class MutationSpaceCleaner(sim.PyOperator):
    """Clean histories of mutations periodically.

    Prune the histories of mutations by removing those associated
    with already extinct alleles.  This reduces memory footprint.
    """

    def __init__(self, *args, **kwargs):
        """Initialize Cleaner object.

        Arguments:
        *args, **kwargs: pass to PyOperator.
        """
        sim.PyOperator.__init__(self, func = self.cleaner, *args, **kwargs)

    def cleaner(self, pop):
        """Obtain list of extant genes, and remove histories of extinct genes.

        Arguments:
        pop: Population object
        """
        # global history
        # global current_max_allele

        global mutation
        for chrom in range(4):
            genes = get_genes(pop, chrom)
            # Get rid of mutation history regarding to extinct
            # alleles.
            # history[chrom], current_max_allele[chrom], name_map = \
            #     clean_up_mutation(genes, history[chrom])
            name_map = mutation.prune(chrom, genes)
            rename_alleles(pop, chrom, name_map)
        return True
