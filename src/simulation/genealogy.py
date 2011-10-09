# -*- mode: python; coding: utf-8; -*-

# genalogy.py - Genealogy

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
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from simulation.exception import SizeError
from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA

class Level(object):

    def __init__(self, parents, time):
        self._lineages = {i:j for i, j in enumerate(parents)}
        self._level = len(self._lineages)
        self._time = time

    def update(self, indecies):
        self._lineages = {i: self._lineages[i]
                          for i in set(indecies)}
        # removed = set(self._lineages) - set(indecies)
        # for r in removed:
        #     del self._lineages[r]
        self._level = len(self._lineages)

    def changeParents(self, lineages):
        l = self._lineages
        for lineage in self._lineages.keys():
            l[lineage] = lineages[l[lineage]]

    def listOfParents(self):
        return [self._lineages[i] for i in sorted(self._lineages)]

    @property
    def level(self):
        return self._level

    @property
    def time(self):
        return self._time

    @property
    def lineages(self):
        return self._lineages


class Genealogy(object):

    def __init__(self, pop_size, chromType):
        # Generate an original level with enough space to hold
        # autosomal markers regardless of chromType.  Otherwise,
        # subsequent generation would refer to invalid parents.
        if chromType == AUTOSOME:
            self._pop_size = 2 * pop_size
        elif chromType == CHROMOSOME_X:
            self._pop_size = 3 * pop_size / 2
        elif chromType == CHROMOSOME_Y:
            self._pop_size = pop_size / 2
        else:
            self._pop_size = pop_size

        self._chromType = chromType
        self.clear()

    def clear(self):
        self._levels = [Level(range(self._pop_size), 0)]
        self._time = 0

    def set(self, parents):
        len_parents = len(parents)
        if len_parents != self._pop_size:
            raise SizeError(self._pop_size, len_parents)
        self._time += 1
        new_level = Level(parents, self._time)
        parent_set = set(parents)
        for level in reversed(self._levels):
            # At least one coalescence occurred during this
            # generation.

            if len(parent_set) != level.level:
                level.update(parents)
                parents = level.listOfParents()
                parent_set = set(parents)
            else:
                break

        removed = []
        for i, level in enumerate(self._levels[:-1]):
            if level.level == self._levels[i+1].level:
                # removed.append(i+1)
                # Remove a duplicate level that is further back in time.
                removed.append(i)

        self._levels.append(new_level)

        for r in removed:
            self._levels[r+1].changeParents(self._levels[r].lineages)

        self._levels = [j for i,j in enumerate(self._levels)
                        if i not in removed]


    @property
    def chromType(self):
        return self._chromType

    def numLevels(self):
        return len(self._levels)

    @property
    def topLevel(self):
        return self._levels[0].level

    @property
    def levels(self):
        return self._levels



if __name__ == '__main__':

    g = Genealogy(10)
    p = range(10)
    g.set(p)
    p = range(10)
    g.set(p)
    p = [0,0,2,2] + range(4,10)
    g.set(p)
    p = [0,0,2,2] + range(4,10)
    g.set(p)
    for i in range(len(g._levels)):
        print(g._levels[i].time, g._levels[i].level, g._levels[i]._lineages)

    g = Genealogy(10)
    p = [0,1,2,3,4,4,4,7,7,9]
    g.set(p)
    p = [1,2,0,2,3,4,5,6,7,8]
    g.set(p)
    p = [0,0,2,2,4,5,6,7,8,9]
    g.set(p)
    for i in range(len(g._levels)):
        print(g._levels[i].time, g._levels[i].level, g._levels[i]._lineages)

    g = Genealogy(10)
    p = [0,0,2,2,4,4,6,6,8,8]
    g.set(p)
    p = [0,0,0,0,0,0,7,7,7,7]
    g.set(p)
    for i in range(len(g._levels)):
        print(g._levels[i].time, g._levels[i].level, g._levels[i]._lineages)


