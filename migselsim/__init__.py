# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import CommandPlugin as cp
from migselsim.baseparser import parser
from migselsim.log import logger

def main():
    # special case. When no argument is given print help.
    if len(sys.argv[1:]) == 0:
        parser.parse_args(['-h'])

    try:
        cp.scan()
    except Exception as e:
        logger.error("Unknown error: `{}`".format(e))

    args = parser.parse_args(sys.argv[1:])
    command = args.command.lower()
    try:
        cp.plugins[command].execute(args)
    except Exception:
        logger.error("Unknown command: `{}`".format(command))
