# -*- mode: python; coding: utf-8; -*-

# tree_gen.py - brief description

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

from __future__ import print_function
import argparse, operator, random

from post_processing import parse_common_arguments, chrom_type, adjust_pop_sizes, run

class Node(object):

    def __init__(self, idx, deme, time, children):
        self._time = time
        self._children = children
        self._idx = idx
        self._deme = deme
        self._parent = None

    @property
    def time(self):
        return self._time

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def idx(self):
        return self._idx

    @property
    def deme(self):
        return self._deme

def generate_trees(data, size1, size2, pop_sizes, mode):
    pop_size = len(data[-1][-1])
    pop_size1 = pop_sizes[0]
    sample1 = random.sample(range(pop_size1), size1)
    sample2 = random.sample(range(pop_size1, pop_size), size2)
    histories = [sample1 + sample2]
    sample_size = len(histories[0])
    level = len(histories[0])
    levels = [sample_size]
    times = [data[-1][0]]
    index = -1

    while level > 1:
        histories.append([-1] * sample_size)
        for i, sample in enumerate(histories[-2]):
            histories[-1][i] = data[index][-1][sample]
        level = len(set(histories[-1]))
        levels.append(level)
        times.append(data[index-1][0])
        index -= 1

    level = 0

    levels = [0] + [i for i in range(1, len(levels))
                    if levels[i] == levels[i - 1] - 1]

    histories = [[histories[j][i] for j in range(len(histories))
                  if j in levels]
                 for i in range(len(histories[0]))]
    t = times[0]
    times = [(t - times[i]) / float(pop_size) for i in range(len(times))
             if i in levels]

    # histories = [[449, 716, 1145, 1638, 978, 143, 1460, 846],
    #              [633, 670, 1222, 1213, 116, 1190, 1460, 846],
    #              [657, 1083, 1993, 1626, 1759, 1629, 1473, 846],
    #              [874, 1981, 1739, 1626, 1759, 1629, 1473, 846],
    #              [995, 953, 1993, 1626, 1759, 1629, 1473, 846],
    #              [1668, 1046, 415, 1626, 1759, 1629, 1473, 846],
    #              [1861, 1786, 1417, 74, 978, 143, 1460, 846],
    #              [1699, 714, 1667, 882, 1499, 1190, 1460, 846],
    #              [1014, 953, 1993, 1626, 1759, 1629, 1473, 846],
    #              [1188, 515, 554, 882, 1499, 1190, 1460, 846]]
    # time = [0.0, 0.0045, 0.0165, 0.087, 0.139, 0.3195, 0.364, 0.7165]

    # histories = [[158, 373, 20, 134],
    #              [180, 92, 90, 134],
    #              [264, 92, 90, 134],
    #              [214, 378, 20, 134]]
    # times = [0, 18, 50, 829] / float(pop_size)

    # histories = [[21, 39, 173, 181],
    #              [143, 298, 364, 181],
    #              [212, 323, 364, 181],
    #              [281, 323, 364, 181]]
    # times = [0.0, 0.24, 0.2925, 1.89]

    dist = {(i,j): len([1 for k,l in zip(histories[i], histories[j])
                        if k != l])
            for i in range(sample_size - 1)
            for j in range(i + 1, sample_size)}

    nodes = [Node(i, 1, times[0], []) for i in range(size1)]
    nodes += [Node(i, 2, times[0], []) for i in range(size1, sample_size)]

    index = sample_size
    for d in sorted(dist.iteritems(), key = operator.itemgetter(1)):
        leaves, distance = d[0], d[1]
        time = times[distance]
        anc0 = find_most_distant_ancestor(leaves[0], time, nodes)
        anc1 = find_most_distant_ancestor(leaves[1], time, nodes)
        if anc0.parent is not None and anc1.parent is not None:
            pass
        elif anc0.parent is not None:
            if anc0.parent is not anc1:
                anc0.parent.children.append(anc1)
                anc1.parent = anc0

        elif anc1.parent is not None:
            if anc1.parent is not anc0:
                anc1.parent.children.append(anc0)
                anc0.parent = anc1
        else:
            deme = 1 if histories[leaves[0]][distance] < pop_size1 else 2
            if anc0 != anc1:
                nodes.append(Node(index, deme, times[distance], [anc0, anc1]))
                anc0.parent = nodes[-1]
                anc1.parent = nodes[-1]
                index += 1
            else:
                nodes.append(Node(index, deme, times[distance], [anc0]))
                anc0.parent = nodes[-1]
                index += 1

    try:
        print(str_sub_tree(nodes[-1], mode), ';', sep='')
    except:
        for i, hist in enumerate(histories):
            print(i, hist)
        print(times)
        for node in nodes:
            print(node.idx, [c.idx for c in node.children])
        raise Exception("circular structure found!")


def str_sub_tree(node, name_internal = False):
    string = ''
    children = node.children
    if len(children) >= 2:
        string += '('
        for child in children[:-1]:
            string += str_sub_tree(child, name_internal)
            string += ','
        string += str_sub_tree(children[-1], name_internal)
        string += ')'
        if name_internal is True:
            string += str(node.idx) + '@' + str(node.deme)
        if node.parent is not None:
            string += ':' + str(node.parent.time - node.time)
    elif len(children) == 0:
        string += str(node.idx) + '@' + str(node.deme)
        string += ':' + str(node.parent.time - node.time)
    return string


def find_most_distant_ancestor(idx, time, nodes):
    hit = None

    # First, find a terminal node with a proper idx.
    hit = [n for n in nodes if n.idx == idx][0]
    # Then, go up its ancestors and find the most distant one with a
    # restriction of node.time < time.
    parent = hit.parent
    while parent is not None and parent.time < time:
        if parent.parent is not None and parent.parent.time < time:
            parent = parent.parent
        else:
            break

    if parent is None:
        return hit
    else:
        return parent


def build_tree(f, args, chrom, pop_sizes):
    for line in f:
        # Skip over a line, which contains the seed for a simulation run.
        line = f.next()
        data = eval(line)
        for r in range(args.reps):
            generate_trees(data[chrom],
                           args.size1,
                           args.size2,
                           pop_sizes,
                           args.internal)

if __name__ == '__main__':
    parser = parse_common_arguments('Construct gene tree.')
    parser.add_argument('-i', '--internal',
                        action = 'store_true',
                        help = 'output names of internal nodes')
    run(parser.parse_args(), build_tree)
