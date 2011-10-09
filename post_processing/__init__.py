# -*- mode: python; coding: utf-8; -*-

# __init__.py - Common functions for post-processing simulation results.

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

def parse_common_arguments():
    parser = argparse.ArgumentParser(description = 'Generate gene tree.')
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

    return parser

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

def run(args, func):
        # Skip over the first line, which contain simulation parameters.
    f = args.file
    line = f.next()
    regex = re.match('Pop Size: \d+\|(\d+) \d+\|(\d+)', line)
    pop_sizes = [int(i) for i in regex.group(1, 2)]
    chrom = chrom_type(args.chrom)
    pop_sizes = adjust_pop_sizes(chrom, pop_sizes)

    # Name internal nodes.  Note that some programs such as seq-gen
    # cannot handle trees with named internal nodes.  Use with this
    # option with care
    if args.seed:
        random.seed(args.seed)

    func(f, args, chrom, pop_sizes)
