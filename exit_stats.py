# -*- mode: python; coding: utf-8; -*-

# exit_stats.py - Exit states and waiting time given initial condition

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

import argparse, random

def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Convert simulation results to exit states and waiting time')
    parser.add_argument('file',
                        type = open,
                        help = 'name of an input file')
    parser.add_argument('size1',
                        type = int,
                        help = 'sample size taken from the first deme')
    parser.add_argument('size2',
                        type = int,
                        help = 'sample size taken from the second deme')
    parser.add_argument('-c', '--chrom',
                        type = str,
                        required = True,
                        help = 'type of chromosome',
                        choices = ['a', 'A', 'x', 'X', 'y', 'Y', 'mt', 'Mt'])
    parser.add_argument('-r', '--reps',
                        type = int,
                        required = False,
                        default = 1,
                        help = 'number of trees per simulated data')
    parser.add_argument('-s', '--seed',
                        type = int)
    return parser.parse_args()


def run(args):
    # Skip over the first line, which contain simulation parameters.
    f = args.file
    f.next()

    if args.seed:
        random.seed(args.seed)
    print('time, #blue in d1, #yellow in d1, deme, type')
    for line in f:
        line = f.next()
        data = eval(line)
        for r in range(args.reps):
            chrom = chrom_type(args.chrom)
            status = exit_states(data[chrom],
                              args.size1,
                              args.size2)
            while status is False:
                status = exit_states(data[chrom],
                                     args.size1,
                                     args.size2)

def exit_states(data, size1, size2):
    pop_size = len(data[-1][-1])
    sample1 = random.sample(range(pop_size / 2), size1)
    sample2 = random.sample(range(pop_size / 2, pop_size), size2)
    level = size1 + size2
    orig_level = level
    histories = [sample1 + sample2]
    index = -1
    while orig_level == level:
        histories.append(
            [data[index][-1][s] for i, s in enumerate(histories[-1])])
        index -= 1
        level = len(set(histories[-1]))

    coal_gen = histories[-1]

    if level + 1 != orig_level:
        return False
    time = (data[-1][0] - data[-len(histories)][0]) / float(pop_size)
    marged = [i for i in set(coal_gen)
              if coal_gen.count(i) == 2][0]
    unchanged = [0, 0]

    for s1 in coal_gen[:size1]:
        if s1 < pop_size / 2 and s1 != marged:
            unchanged[0] += 1
    for s2 in coal_gen[size1:]:
        if s2 < pop_size / 2 and s2 != marged:
            unchanged[1] += 1

    marged1 = coal_gen.index(marged)
    marged2 = coal_gen.index(marged, marged1 + 1)
    if marged1 < size1 and marged2 < size1:
        ctype = 0
    elif marged1 < size1:
        ctype = 1
    else:
        ctype = 2
    if marged < pop_size / 2:
        deme = 1
    else:
        deme = 2

    print('{}, {}, {}, {}, {}'.format(
        time, unchanged[0], unchanged[1], deme, ctype))
    return True

def chrom_type(chrom):
    if chrom == 'a' or chrom == 'A':
        return 0
    elif chrom == 'x' or chrom == 'X':
        return 1
    elif chrom == 'y' or chrom == 'Y':
        return 2
    else:
        return 3


if __name__ == '__main__':
    args = parse_arguments()
    run(args)
