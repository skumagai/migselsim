# -*- mode: python; coding: utf-8; -*-

# mutation.py - brief description

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
from simulation.mutation import Mutation

class TestMutation(unittest.TestCase):

    def setUp(self):
        self.mut = Mutation()
        self.mut._hist[0] = {0: [None],
                             1: [None, 0],
                             2: [None, 0, 1],
                             3: [None, 0],
                             4: [None, 0, 3],
                             5: [None, 0, 1, 2],
                             6: [None, 0, 1, 2],
                             7: [None, 0, 1, 2, 5],
                             8: [None, 0, 1, 2, 6]}
        self.mut._max[0] = len(self.mut.history(0))

    def testInit(self):
        mut = Mutation()
        for chrom in range(4):
            self.assertEqual(mut.numAlleles(chrom), 1)
            self.assertEqual(mut.history(chrom), {0: [None]})

    def testAddAllele(self):
        mut = Mutation()
        for chrom in range(4):
            mut.addAllele(chrom, 0)
            self.assertEqual(mut.numAlleles(chrom), 2)

        mut.addAllele(0, 0)
        self.assertEqual(mut.numAlleles(0), 3)

    def testHistory(self):
        mut = Mutation()
        mut.addAllele(0, 0)
        mut.addAllele(0, 0)
        mut.addAllele(0, 2)
        mut.addAllele(0, 2)
        hist = mut.history(0)
        self.assertEqual(mut.numAlleles(0), 5)
        self.assertEqual(mut.history(0),
                         {0: [None],
                          1: [None, 0],
                          2: [None, 0],
                          3: [None, 0, 2],
                          4: [None, 0, 2]})

    def testClear(self):
        self.mut.addAllele(0, 0)
        self.mut.clear()
        for chrom in range(4):
            self.assertEqual(self.mut.numAlleles(chrom), 1)
            self.assertEqual(self.mut.history(chrom), {0: [None]})

    def testPruneMonomorphic(self):
        self.mut.prune(0, [7])
        self.assertEqual(self.mut.history(0),
                         {0: [None]})
        self.assertEqual(self.mut.numAlleles(0), 1)

    def testPruneRecentSplit(self):
        self.mut.prune(0, [7, 8])
        self.assertEqual(self.mut.history(0),
                         {3: [None, 0, 1],
                          4: [None, 0, 2]})
        self.assertEqual(self.mut.numAlleles(0), 5)

    def testPruneAncentSplit(self):
        self.mut.prune(0, [3, 7])
        self.assertEqual(self.mut.history(0),
                         {3: [None, 0],
                          5: [None, 0, 1, 2, 4]})
        self.assertEqual(self.mut.numAlleles(0), 6)


    def testPairwiseDistance(self):
        expected = {(0, 1): 1,
                    (0, 2): 2,
                    (0, 3): 1,
                    (0, 4): 2,
                    (0, 5): 3,
                    (0, 6): 3,
                    (0, 7): 4,
                    (0, 8): 4,
                    (1, 2): 1,
                    (1, 3): 2,
                    (1, 4): 3,
                    (1, 5): 2,
                    (1, 6): 2,
                    (1, 7): 3,
                    (1, 8): 3,
                    (2, 3): 3,
                    (2, 4): 4,
                    (2, 5): 1,
                    (2, 6): 1,
                    (2, 7): 2,
                    (2, 8): 2,
                    (3, 4): 1,
                    (3, 5): 4,
                    (3, 6): 4,
                    (3, 7): 5,
                    (3, 8): 5,
                    (4, 5): 5,
                    (4, 6): 5,
                    (4, 7): 6,
                    (4, 8): 6,
                    (5, 6): 2,
                    (5, 7): 1,
                    (5, 8): 3,
                    (6, 7): 3,
                    (6, 8): 1,
                    (7, 8): 4}
        self.assertEqual(self.mut.pairwiseDistance(0), expected)

    def testPairwiseDistanceAfterPrune(self):
        self.mut.prune(0, [7, 8])
        expected = {(3, 4): 4}
        self.assertEqual(self.mut.pairwiseDistance(0), expected)
