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

import argparse, random, re

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
    line = f.next()
    regex = re.match('Pop Size: \d+\|(\d+) \d+\|(\d+)', line)
    pop_sizes = [int(i) for i in regex.group(1, 2)]
    chrom = chrom_type(args.chrom)
    pop_sizes = adjust_pop_sizes(chrom, pop_sizes)

    if args.seed:
        random.seed(args.seed)
    print('time, #blue in d1, #yellow in d1, deme, type')
    for line in f:
        line = f.next()
        data = eval(line)
        for r in range(args.reps):
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
    merged = [i for i in set(coal_gen)
              if coal_gen.count(i) == 2][0]
    unchanged = [0, 0]

    for s1 in coal_gen[:size1]:
        if s1 < pop_size / 2 and s1 != merged:
            unchanged[0] += 1
    for s2 in coal_gen[size1:]:
        if s2 < pop_size / 2 and s2 != merged:
            unchanged[1] += 1

    merged1 = coal_gen.index(merged)
    merged2 = coal_gen.index(merged, merged1 + 1)
    if merged1 < size1 and merged2 < size1:
        ctype = 0
    elif merged1 < size1:
        ctype = 1
    else:
        ctype = 2
    if merged < pop_size / 2:
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

def adjust_pop_sizes(chrom, pop_sizes):
    if chrom == 0:
        return [i * 2 for i in pop_sizes]
    elif chrom == 1:
        return [i * 3 / 2 for i in pop_sizes]
    elif chrom == 2:
        return [i / 2 for i in pop_sizes]
    else:
        return pop_sizes


if __name__ == '__main__':
    args = parse_arguments()
    run(args)
