# -*- mode: python; coding: utf-8; -*-

# test_genealogy_tracker.py - Unit test file for genealogy_tracker.py

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

import simuOpt
simuOpt.setOptions(
    quiet = True,
    alleleType = 'long')

import genealogy as genea

genealogy = [genea.Genealogy(24)]

class Reindexer(sim.PyOperator):

    def __init__(self, loci, *args, **kwargs):
        self._loci = loci
        sim.PyOperator.__init__(self, func = self.reindex, *args, **kwargs)

    def reindex(self, pop):
        loci = self._loci
        marker = loci[0]
        j = 0
        for i, ind in enumerate(pop.individuals()):
            ind.setAllele(2 * i, marker,
                          ploidy = 0, chrom = j)
            ind.setAllele(2 * i + 1, marker,
                          ploidy = 1, chrom = j)
        return True


def run():
    pop = sim.Population(size = [6, 6],
                         loci = [1],
                         infoFields = 'migrate_to')

    pop.setVirtualSplitter(sim.SexSplitter())

    s = sim.Simulator(pop)

    s.evolve(
        initOps = [sim.InitSex(sex = [sim.MALE, sim.FEMALE],
                               subPops = 0),
                   sim.InitSex(sex = [sim.MALE, sim.FEMALE],
                               subPops = 1),
                   sim.InitGenotype(genotype=range(24)),
                   sim.Dumper()],
        preOps = [sim.Migrator(rate=[[0.9, 0.1],[0.1,0.9]])],
        matingScheme = sim.RandomMating(
            subPopSize = [6, 6],
            sexMode = (sim.GLOBAL_SEQUENCE_OF_SEX, sim.MALE, sim.FEMALE)),
        postOps = [Tracker([0]), Reindexer([0])],
        finalOps = [sim.Dumper()])

if __name__ == '__main__':
    run()


