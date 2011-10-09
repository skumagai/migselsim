# -*- mode: python; coding: utf-8; -*-

# test_summary_stat.py - brief description

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
import math

from simulation.mutation import Mutation
from simulation import summary_stat as st

class TestFstEqualPopSizes(unittest.TestCase):

    def setUp(self):
        self.mut = Mutation()
        self.mut._hist[0] = {0: [None],
                             5: [None, 0, 1, 2, 3, 4],
                             15: [None, 0, 6, 7, 8, 9, 10, 11, 12, 13, 14]}

    def testNoVariationInOneDeme(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [15] * 10,
                                          self.mut,
                                          [(2, 3), (2, 3)], 0),
                               0.6900584795321637)

    def testVariationInBothDeme(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 2,
                                          self.mut,
                                          [(2, 3), (2, 3)], 0),
                               -0.11111111111111)


    def testNoVariationInBothDemes1(self):
        self.assertTrue(math.isnan(st.Fst.get([0] * 10 + [0] * 10,
                                              self.mut,
                                              [(2, 3), (2, 3)], 0)))

    def testNoVariationInBothDemes2(self):
        self.assertAlmostEqual(st.Fst.get([0] * 10 + [5] * 10,
                                          self.mut,
                                          [(2, 3), (2, 3)], 0),
                               1.)


class TestFstUnequalPopSizes(unittest.TestCase):

    def setUp(self):
        self.mut = Mutation()
        self.mut._hist[0] = {0: [None],
                             5: [None, 0, 1, 2, 3, 4],
                             15: [None, 0, 6, 7, 8, 9, 10, 11, 12, 13, 14]}

    def testNoVariationInOneDeme(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [15] * 14,
                                          self.mut,
                                          [(2, 3), (3, 4)], 0),
                               0.794891640866873)

    def testVariationInBothDeme(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 6,
                                          self.mut,
                                          [(2, 3), (3, 4)], 0),
                               -0.02941176470588247)


    def testNoVariationInBothDemes1(self):
        self.assertTrue(math.isnan(st.Fst.get([0] * 10 + [0] * 14,
                                              self.mut,
                                              [(2, 3), (3, 4)], 0)))

    def testNoVariationInBothDemes2(self):
        self.assertAlmostEqual(st.Fst.get([0] * 10 + [5] * 14,
                                          self.mut,
                                          [(2, 3), (3, 4)], 0),
                               1.)

    def testMssingAlleles(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 5 +
                                          [0] * 5 + [15] * 9,
                                          self.mut,
                                          [(2, 3), (3, 4)], 0),
                               0.5264705882352942)


class TestDifferentChromosomes(unittest.TestCase):
    def setUp(self):
        self.mut = Mutation()
        for chrom in range(4):
            self.mut._hist[chrom] = {
                0: [None],
                5: [None, 0, 1, 2, 3, 4],
                15: [None, 0, 6, 7, 8, 9, 10, 11, 12, 13, 14]}

    def testAutosome(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 2,
                                          self.mut,
                                          [(2, 3), (2, 3)], 0),
                               -0.11111111111111)

    def testX(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 2,
                                          self.mut,
                                          [(2, 4), (4, 3)], 1),
                               -0.11111111111111)

    def testY(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 2,
                                          self.mut,
                                          [(10, 0), (10, 0)], 2),
                               -0.11111111111111)

    def testMitochondria(self):
        self.assertAlmostEqual(st.Fst.get([0] * 5 + [5] * 3 + [15] * 2 +
                                          [0] * 5 + [5] * 3 + [15] * 2,
                                          self.mut,
                                          [(4, 6), (3, 7)], 3),
                               -0.11111111111111)



class TestAveragePairwiseDifferenceWithin(unittest.TestCase):

    def setUp(self):
        self.dist = {(1, 2): 10,
                     (1, 3): 5,
                     (2, 3): 15}

    def testNoVariationInOneDeme(self):
        counts = [{1: 5, 2: 3, 3: 2}, {1:0, 2:0, 3: 15}]
        denom = 9 * 5 + 15 * 7
        self.assertAlmostEqual(st.measure_variation_within(self.dist,
                                                           counts,
                                                           denom),
                               1.9333333333333333)

    def testVariationInBothDeme(self):
        counts = [{1:5, 2: 3, 3: 2}, {1: 5, 2: 3, 3: 2}]
        denom = 90
        self.assertAlmostEqual(st.measure_variation_within(self.dist,
                                                           counts,
                                                           denom),
                               6.444444444444445)


    def testNoVariationInBothDemes1(self):
        counts = [{1: 10}, {1: 10}]
        denom = 90
        self.assertAlmostEqual(st.measure_variation_within(self.dist,
                                                           counts,
                                                           denom),
                               0.0)


    def testNoVariationInBothDemes2(self):
        counts = [{1: 10}, {2: 10}]
        denom = 90
        self.assertAlmostEqual(st.measure_variation_within(self.dist,
                                                           counts,
                                                           denom),
                               0.0)


class TestAveragePairwiseDifferenceBetween(unittest.TestCase):

    def setUp(self):
        self.dist = {(1, 2): 10,
                     (1, 3): 5,
                     (2, 3): 15}

    def testNoVariationInOneDeme(self):
        counts = [{1: 5, 2: 3, 3: 2}, {1:0, 2:0, 3: 15}]
        denom = 150
        self.assertAlmostEqual(st.measure_variation_between(self.dist,
                                                            counts,
                                                            denom),
                               7.0)

    def testVariationInBothDeme(self):
        counts = [{1:5, 2: 3, 3: 2}, {1: 5, 2: 3, 3: 2}]
        denom = 100
        self.assertAlmostEqual(st.measure_variation_between(self.dist,
                                                           counts,
                                                           denom),
                               5.8)


    def testNoVariationInBothDemes1(self):
        counts = [{1: 10}, {1: 10}]
        denom = 100
        self.assertAlmostEqual(st.measure_variation_between(self.dist,
                                                           counts,
                                                           denom),
                               0.0)


    def testNoVariationInBothDemes2(self):
        counts = [{1: 10}, {2: 10}]
        denom = 100
        self.assertAlmostEqual(st.measure_variation_between(self.dist,
                                                           counts,
                                                           denom),
                               10.0)
