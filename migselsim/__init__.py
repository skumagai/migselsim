# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import all_commands
from migselsim.baseparser import parser

def main():
    # args = parser.parse_args(sys.argv[1:])
    print all_commands

    # command = args[0].lower()
    # try:
    #     commands = list_all_commands()
    #     commands[command]().execute(args[1:])
    # except:
    #     parser.error("Unknown command: `{}`".format(command))


# from migselsim.configs import parse_config
    # sims = []
    # try:
    #     with open(sys.argv[1], 'r') as f:
    #         stream = f.read()
    #         sims.append(parse_config(stream))
    #     for sim in sims:
    #         pass
    #         # sim.run()
    # except IndexError:
    #     sys.stderr.write("missing config file.")
    #     sys.stderr.flush()
