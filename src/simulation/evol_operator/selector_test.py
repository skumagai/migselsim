# -*- mode: python; coding: utf-8; -*-

# test_selectors.py - brief description

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

import unittest

import simuPOP as sim

from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA
from simulation import get_genes
from simulation.evol_operator.selector import MySelectorProvider

class TestSelector(unittest.TestCase):

    def setUp(self):
        self.fs = 0.9
        self.ms = 0.5
        self.pop = sim.Population(size=[4, 4],
                                  loci=[1, 1, 1, 1],
                                  chromTypes=[sim.AUTOSOME,
                                              sim.CHROMOSOME_X,
                                              sim.CHROMOSOME_Y,
                                              sim.CUSTOMIZED],
                                  infoFields=['fitness'])
        self.pop.setVirtualSplitter(sim.SexSplitter())
        sim.initSex(self.pop, sex=[sim.MALE, sim.FEMALE])
        for i in range(2):
            for j in range(2):
                sim.initGenotype(self.pop,
                                 loci=[0], # Autosome
                                 prop=[0.5, 0.5],
                                 subPops=[(i,j)])
                sim.initGenotype(self.pop,
                                 loci=[3], # Mitochondria
                                 ploidy=0,
                                 prop=[0.5, 0.5],
                                 subPops=[(i,j)])
            sim.initGenotype(self.pop,
                             loci=[1], # Chromosome X
                             prop=[0.5, 0.5],
                             subPops=[(i,1)])
            sim.initGenotype(self.pop,
                             loci=[1], # Chromosome X
                             prop=[0.5, 0.5],
                             ploidy=0,
                             subPops=[(i,0)])
            sim.initGenotype(self.pop,
                             loci=[2], # Chromosome Y
                             prop=[0.5, 0.5],
                             ploidy=1,
                             subPops=[(i,0)])

    def testSingleLocusAutosome(self):
        sel = MySelectorProvider(self.pop, [0], [0], [self.fs], [self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                f = [1.0, self.fs, self.fs**2]
                m = [1.0, self.ms, self.ms**2]
            else:
                f = [self.fs**2, self.fs, 1.0]
                m = [self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                genotype = tuple(ind.allele(0, ploidy=p, chrom=0)
                                 for p in range(2))
                if ind.sex() == sim.FEMALE:
                    if genotype == (0, 0):
                        self.assertAlmostEqual(ind.fitness, f[0])
                    elif genotype == (0, 1) or genotype == (1, 0):
                        self.assertAlmostEqual(ind.fitness, f[1])
                    else:
                        self.assertAlmostEqual(ind.fitness, f[2])
                else:
                    if genotype == (0, 0):
                        self.assertAlmostEqual(ind.fitness, m[0])
                    elif genotype == (0, 1) or genotype == (1, 0):
                        self.assertAlmostEqual(ind.fitness, m[1])
                    else:
                        self.assertAlmostEqual(ind.fitness, m[2])


    def testSingleLocusChromosomeX(self):
        sel = MySelectorProvider(self.pop, [1], [0], [self.fs], [self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                f = [1.0, self.fs, self.fs**2]
                m = [1.0, self.ms]
            else:
                f = [self.fs**2, self.fs, 1.0]
                m = [self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                if ind.sex() == sim.FEMALE:
                    genotype = tuple(ind.allele(0, ploidy=p, chrom=1)
                                     for p in range(2))
                    if genotype == (0, 0):
                        self.assertAlmostEqual(ind.fitness, f[0])
                    elif genotype == (0, 1) or genotype == (1, 0):
                        self.assertAlmostEqual(ind.fitness, f[1])
                    else:
                        self.assertAlmostEqual(ind.fitness, f[2])
                else:
                    genotype = tuple(ind.allele(0, ploidy=0, chrom=1)
                                     for p in range(1))
                    if genotype == (0,):
                        self.assertAlmostEqual(ind.fitness, m[0])
                    else:
                        self.assertAlmostEqual(ind.fitness, m[1])


    def testSingleLocusChromosomeY(self):
        sel = MySelectorProvider(self.pop, [2], [0], [self.fs], [self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                m = [1.0, self.ms]
            else:
                m = [self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                if ind.sex() == sim.MALE:
                    genotype = tuple(ind.allele(0, ploidy=1, chrom=2)
                                     for p in range(1))
                    if genotype == (0,):
                        self.assertAlmostEqual(ind.fitness, m[0])
                    else:
                        self.assertAlmostEqual(ind.fitness, m[1])


    def testSingleLocusMitochondria(self):
        sel = MySelectorProvider(self.pop, [3], [0], [self.fs], [self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                f = [1.0, self.fs]
                m = [1.0, self.ms]
            else:
                f = [self.fs, 1.0]
                m = [self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                genotype = tuple(ind.allele(0, ploidy=p, chrom=3)
                                 for p in range(2))
                if ind.sex() == sim.FEMALE:
                    if genotype == (0, 0):
                        self.assertAlmostEqual(ind.fitness, f[0])
                    else:
                        self.assertAlmostEqual(ind.fitness, f[1])
                if ind.sex() == sim.MALE:
                    if genotype == (0, 0):
                        self.assertAlmostEqual(ind.fitness, m[0])
                    else:
                        self.assertAlmostEqual(ind.fitness, m[1])

    def testTwoLociAX(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 1], [0, 0],
                                 [self.fs, self.fs],
                                 [self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3, self.fs**4]
                m = [1.0, self.ms, self.ms**2, self.ms**3]
            else:
                f = [self.fs**4, self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = p)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])

    def testTwoLociAmt(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 3], [0, 0],
                                 [self.fs, self.fs],
                                 [self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3]
                m = [1.0, self.ms, self.ms**2, self.ms**3]
            else:
                f = [self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                # Mitochondria
                genotype += len([1 for i in
                                 ind.genotype(chroms = [3],
                                              ploidy = 0)
                                 if i == 1])
                if ind.sex() == sim.FEMALE:
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testTwoLociXY(self):
        sel = MySelectorProvider(self.pop,
                                 [1, 2], [0, 0],
                                 [self.fs, self.fs],
                                 [self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2]
                m = [1.0, self.ms, self.ms**2]
            else:
                f = [self.fs**2, self.fs, 1.0]
                m = [self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype = len([1 for p in range(2) for i in
                                    ind.genotype(chroms = [1],
                                                 ploidy = p)
                                    if i == 1])
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype = len([1 for i in
                                    ind.genotype(chroms = [1],
                                                 ploidy = 0)
                                    if i == 1])
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testTwoLociXMt(self):
        sel = MySelectorProvider(self.pop,
                                 [1, 3], [0, 0],
                                 [self.fs, self.fs],
                                 [self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3]
                m = [1.0, self.ms, self.ms**2]
            else:
                f = [self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Mitochondria
                genotype = len([1 for i in
                                ind.genotype(chroms = [3],
                                             ploidy = 0)
                                if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                    ind.genotype(chroms = [1],
                                                 ploidy = p)
                                    if i == 1])
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testTwoLociYMt(self):
        sel = MySelectorProvider(self.pop,
                                 [2, 3], [0, 0],
                                 [self.fs, self.fs],
                                 [self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs]
                m = [1.0, self.ms, self.ms**2]
            else:
                f = [self.fs, 1.0]
                m = [self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Mitochondria
                genotype = len([1 for i in
                                ind.genotype(chroms = [3],
                                             ploidy = 0)
                                if i == 1])
                if ind.sex() == sim.FEMALE:
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])

    def testThreeLociAXY(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 1, 2], [0, 0, 0],
                                 [self.fs, self.fs, self.fs],
                                 [self.ms, self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3, self.fs**4]
                m = [1.0, self.ms, self.ms**2, self.ms**3, self.ms**4]
            else:
                f = [self.fs**4, self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**4, self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = p)
                                     if i == 1])

                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testThreeLociAXMt(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 1, 3], [0, 0, 0],
                                 [self.fs, self.fs, self.fs],
                                 [self.ms, self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3, self.fs**4, self.fs**5]
                m = [1.0, self.ms, self.ms**2, self.ms**3, self.ms**4]
            else:
                f = [self.fs**5, self.fs**4, self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**4, self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                # Mitochondria
                genotype += len([1 for i in
                                 ind.genotype(chroms = [3],
                                              ploidy = 0)
                                 if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = p)
                                     if i == 1])

                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testThreeLociAYMt(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 2, 3], [0, 0, 0],
                                 [self.fs, self.fs, self.fs],
                                 [self.ms, self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3]
                m = [1.0, self.ms, self.ms**2, self.ms**3, self.ms**4]
            else:
                f = [self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**4, self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                # Mitochondria
                genotype += len([1 for i in
                                 ind.genotype(chroms = [3],
                                              ploidy = 0)
                                 if i == 1])
                if ind.sex() == sim.FEMALE:
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])

    def testThreeLociXYMt(self):
        sel = MySelectorProvider(self.pop,
                                 [1, 2, 3], [0, 0, 0],
                                 [self.fs, self.fs, self.fs],
                                 [self.ms, self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3]
                m = [1.0, self.ms, self.ms**2, self.ms**3]
            else:
                f = [self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Mitochondria
                genotype = len([1 for i in
                                 ind.genotype(chroms = [3],
                                              ploidy = 0)
                                 if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = p)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])


    def testFourLociAXYMt(self):
        sel = MySelectorProvider(self.pop,
                                 [0, 1, 2, 3], [0, 0, 0, 0],
                                 [self.fs, self.fs, self.fs, self.fs],
                                 [self.ms, self.ms, self.ms, self.ms])
        selectors = sel.setSelector()
        for s in selectors:
            s.apply(self.pop)
        for i in range(2):
            if i == 0:
                # # of "1" alleles
                f = [1.0, self.fs, self.fs**2, self.fs**3, self.fs**4, self.fs**5]
                m = [1.0, self.ms, self.ms**2, self.ms**3, self.ms**4, self.ms**5]
            else:
                f = [self.fs**5, self.fs**4, self.fs**3, self.fs**2, self.fs, 1.0]
                m = [self.fs**5, self.fs**4, self.ms**3, self.ms**2, self.ms, 1.0]
            for ind in self.pop.individuals(subPop=[i]):
                # Autosome
                genotype = len([1 for p in range(2) for i in
                                ind.genotype(chroms = [0],
                                             ploidy = p)
                                if i == 1])
                # Mitochondria
                genotype += len([1 for i in
                                 ind.genotype(chroms = [3],
                                              ploidy = 0)
                                 if i == 1])
                if ind.sex() == sim.FEMALE:
                    # Chromosome X
                    genotype += len([1 for p in range(2) for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = p)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, f[genotype])
                else:
                    # Chromosome X
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [1],
                                                  ploidy = 0)
                                     if i == 1])
                    # Chromosome Y
                    genotype += len([1 for i in
                                     ind.genotype(chroms = [2],
                                                  ploidy = 1)
                                     if i == 1])
                    self.assertAlmostEqual(ind.fitness, m[genotype])
