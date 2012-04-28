# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import list_all_commands
from migselsim.baseparser import parser

__version__ == 0.0.1

def main():
    options, args = parser.parse_args(sys.argv[1:])
    if options.help and not args:
        args = ['help']
    if not args:
        args = ['help']         # Fallback

    command = args[0].lower()
    try:
        commands = list_all_commands()
        commands[command]().execute(args[1:])
    except:
        parser.error("Unknown command: `{}`".format(command))


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
