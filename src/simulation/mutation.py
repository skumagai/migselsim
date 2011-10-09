# -*- mode: python; coding: utf-8; -*-

# mutation.py - mutation

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

class Mutation(object):
    """Keep track of mutation arisen during forward simulation.
    """

    def __init__(self):
        """
        """
        self.clear()

    def clear(self):
        """Reset mutation information."""
        # Number of alleles in mutation space.
        self._max = [1] * 4
        # Store the entire history of each allele from the ultimate
        # ancestor to the immediate ancestor (parent).
        self._hist = [{0:[None]}] * 4

    def addAllele(self, chrom, allele):
        """Add new allele.

        Arguments:
        chrom: index of chromosome
        allele: an original allele, from which a new allele mutates.
        """
        # Get the state of new allele.
        new_allele = self._max[chrom]

        # Record the current allele as a parent of new allele by first
        # making a clone of evolutionary history of the parental
        # allele and then appending the parental allele at the end of
        # clone.  Cloning is done to make two history not sharing the
        # same list.  Although this increases memory footprint, it is
        # necessary so that pruning extinct allele from memory later
        # does not affect exant alleles.
        self._hist[chrom][new_allele] = list(self._hist[chrom][allele])
        self._hist[chrom][new_allele].append(allele)
        self._max[chrom] += 1
        return new_allele

    def prune(self, chrom, alleles):
        """Eliminate information of extinct alleles

        Arguments:
        chrom: index of chromosome
        alleles: list of extant alleles
        """

        # Eliminate extinct alleles, which do not appear in the list
        # of ancestral alleles for the extant alleles.
        if len(alleles) == 1:
            self.clear()
            return
        new_hist = dict((allele, self._hist[chrom][allele])
                        for allele in self._hist[chrom].keys()
                        if allele in alleles)
        required_alleles = list(set([allele
                                     for anc_alleles in new_hist.values()
                                     for allele in anc_alleles]))
        required_alleles.sort()

        extant = new_hist.keys()
        sextant = set(extant)
        unneeded = set(new_hist[extant[0]])
        for hist in [new_hist[key] for key in extant[1:]]:
            unneeded = unneeded.intersection(hist)
        unneeded = list(unneeded)
        unneeded.sort()
        unneeded.pop()
        required_alleles = [allele
                            for allele in required_alleles
                            if allele not in unneeded and
                               allele not in sextant]

        required_alleles.extend(
            [extant_allele for extant_allele in extant])
        required_alleles = list(set(required_alleles))
        required_alleles.sort()

        new_hist = dict((key,
                         [allele for allele in new_hist[key]
                          if allele in required_alleles])
                        for key in extant)

        # Construct a mapping of old ids to new ids.
        name_map = dict((orig_name, new_name)
                        for new_name, orig_name
                        in enumerate(required_alleles))

        # Replace names in history
        self._hist[chrom] = dict((name_map[name],
                                  [None] +
                                  [name_map[anc] for anc in new_hist[name]])
                                 for name in extant)
        self._max[chrom] = max(self._hist[chrom]) + 1

        return name_map

    def history(self):
        """ """
        return self._hist

    def history(self, chrom):
        """Returns history of mutation

        Arguments:
        chrom: index of chromosome
        """
        return self._hist[chrom]

    def numAlleles(self):
        """ """
        return self._max

    def numAlleles(self, chrom):
        """Returns number of allels in the current mutaiton space.

        Arguments:
        chrom: index of chromosome
        """
        return self._max[chrom]


    def pairwiseDistance(self, chrom):
        """Compute pairwise distance between two sequences.

        Arguments:
        chrom: index of chromosome
        """
        dist = dict()
        history = self.history(chrom)
        sorted_alleles = sorted(history.keys())

        # If a population is monomorphic, there is nothing to do.
        if len(sorted_alleles) == 1:
            return dist

        # When allele "0" (the original allele) is present, expression
        # for pairwise distances are slightly different from other
        # cases.
        if 0 == sorted_alleles[0]:
            for allele1 in sorted_alleles[1:]:
                dist[(0, allele1)] = len(history[allele1]) - 1
            for index0, allele0 in enumerate(sorted_alleles[1:-1]):
                for allele1 in sorted_alleles[index0+2:]:
                    shared = set(history[allele0]).intersection(
                        set(history[allele1]))
                    if allele0 in history[allele1]:
                        dist[(allele0, allele1)] = len(
                            history[allele1][
                                history[allele1].index(allele0):])
                    else:
                        l0 = len(history[allele0][
                                history[allele0].index(max(shared)):])
                        l1 = len(history[allele1][
                                history[allele1].index(max(shared)):])
                        dist[(allele0, allele1)] = l0 + l1
        else:
            for index0, allele0 in enumerate(sorted_alleles[:-1]):
                for allele1 in sorted_alleles[index0+1:]:
                    shared = set(history[allele0]).intersection(
                        set(history[allele1]))
                    if allele0 in history[allele1]:
                        dist[(allele0, allele1)] = len(
                            history[allele1][
                                history[allele1].index(allele0):])
                    else:
                        l0 = len(history[allele0][
                                history[allele0].index(max(shared)):])
                        l1 = len(history[allele1][
                                history[allele1].index(max(shared)):])
                        dist[(allele0, allele1)] = l0 + l1
        return dist
