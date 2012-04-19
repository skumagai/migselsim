# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.configs import parse_config

def main():
    sims = []
    try:
        with open(sys.argv[1], 'r') as f:
            stream = f.read()
            sims.append(parse_config(stream))
        for sim in sims:
            pass
            # sim.run()
    except IndexError:
        sys.stderr.write("missing config file.")
        sys.stderr.flush()
