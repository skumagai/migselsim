# -*- mode: python; coding: utf-8; -*-

# test___init__.py - brief description

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

from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA
from simulation import get_genes, rename_alleles

import simuPOP as sim

class TestGetGenes(unittest.TestCase):

    def setUp(self):
        self.pop = sim.Population(size=[10, 20],
                                  loci=[1, 1, 1, 1],
                                  chromTypes=[sim.AUTOSOME,
                                              sim.CHROMOSOME_X,
                                              sim.CHROMOSOME_Y,
                                              sim.CUSTOMIZED])
        self.pop.setVirtualSplitter(sim.SexSplitter())
        sim.initSex(self.pop, sex=[sim.MALE, sim.FEMALE])
        sim.initGenotype(self.pop, prop=[1.0, 0.0], subPops=0)
        sim.initGenotype(self.pop, prop=[0.0, 1.0], subPops=1)

    def testAutosome(self):
        genes = get_genes(self.pop, AUTOSOME, 0)
        self.assertEqual(genes, [0] * 20 + [1] * 40)

    def testChrX(self):
        genes = get_genes(self.pop, CHROMOSOME_X, 0)
        self.assertEqual(genes, [0] * 15 + [1] * 30)

    def testChrY(self):
        genes = get_genes(self.pop, CHROMOSOME_Y, 0)
        self.assertEqual(genes, [0] * 5 + [1] * 10)

    def testMitochondria(self):
        genes = get_genes(self.pop, MITOCHONDRIA, 0)
        self.assertEqual(genes, [0] * 10 + [1] * 20)


class TestRenameAlleles(unittest.TestCase):

    def setUp(self):
        self.pop = sim.Population(size=[10, 20],
                                  loci=[2])
        self.pop.setVirtualSplitter(sim.SexSplitter())
        sim.initSex(self.pop, sex=[sim.MALE, sim.FEMALE])
        sim.initGenotype(self.pop,
                         loci = [1],
                         prop=[0.0, 0.0, 0.0, 0.0, 0.4, 0.4, 0.2],
                         subPops=0)
        sim.initGenotype(self.pop,
                         loci = [1],
                         prop=[0.0, 0.0, 0.0, 0.4, 0.0, 0.2, 0.4],
                         subPops=1)

    def test_rename_alleles(self):
        name_map = {3: 1,
                    4: 2,
                    5: 3,
                    6: 4}
        orig_genes = get_genes(self.pop, AUTOSOME, 1)
        rename_alleles(self.pop, 0, name_map)
        new_genes = get_genes(self.pop, AUTOSOME, 1)
        for og, ng in zip(orig_genes, new_genes):
            self.assertEqual(og, ng + 2)

