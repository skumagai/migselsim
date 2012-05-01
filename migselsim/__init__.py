# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import all_commands
from migselsim.baseparser import parser

def main():
    # special case. When no argument is given print help.
    if len(sys.argv[1:]) == 0:
        parser.parse_args(['-h'])

    args = parser.parse_args(sys.argv[1:])

    command = args.command.lower()
    try:
        all_commands[command].execute(args)
    except Exception:
        parser.error("Unknown command: `{}`".format(command))
