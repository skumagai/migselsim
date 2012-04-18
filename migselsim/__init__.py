# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.baseconfig import parse_config

def main():
    with open(sys.argv[1], 'r') as f:
        stream = f.read()
        parse_config(stream)
