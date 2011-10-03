# -*- mode: python; coding: utf-8; -*-

# track_genealogy.py - Development of tracking gene genealogy in
# simuPOP simulations.

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
from simulation import genealogies
from simulation.exception import SizeError
from simulation import genealogy

class GenealogyTracker(sim.PyOperator):

    def __init__(self,
                 loci = [],
                 chroms = [],
                 *args, **kwargs):
        self._loci = loci
        self._chroms = chroms
        global genealogies
        if len(genealogies) != len(self._loci):
            raise SizeError(len(genealogies), len(self._loci))

        sim.PyOperator.__init__(self, func = self.track, *args, **kwargs)

    def track(self, pop):
        global genealogies
        loci = self._loci
        for i, locus in enumerate(loci):
            if genealogies[i].chromType is AUTOSOME:
                state = [ind.allele(locus, ploidy = p, chrom = AUTOSOME)
                         for ind in  pop.individuals()
                         for p in [0,1]]
            elif genealogies[i].chromType is CHROMOSOME_X:
                state = [ind.allele(locus, ploidy = p, chrom = CHROMOSOME_X)
                         for ind in pop.individuals()
                         for p in [0,1]
                         if ind.sex() == sim.FEMALE or p == 0]
            elif genealogies[i].chromType is CHROMOSOME_Y:
                state = [ind.allele(locus, ploidy = 1, chrom = CHROMOSOME_Y)
                         for ind in pop.individuals()
                         if ind.sex() == sim.MALE]
            else:
                state = [ind.allele(locus, ploidy = 0, chrom = MITOCHONDRIA)
                         for ind in pop.individuals()]

            # state holds parental ID.
            genealogies[i].set(state)

        if all([g.topLevel == 1 for g in genealogies]):
            print({g.chromType:
                       [(level.time, level.level, level.lineages)
                        for level in g.levels]
                   for g in genealogies})
            for g in genealogies:
                g.clear()
            return False
        else:
            return True


# Utility functions
def init_genealogies(pop_size, chroms):
    global genealogies
    for chrom in chroms:
        genealogies.append(genealogy.Genealogy(pop_size, chrom))

