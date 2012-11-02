# -*- mode: python; coding: utf-8; -*-

import sys
import os.path

from migselsim.baseparser import command_parsers, parser
from migselsim.model import Model
from migselsim.simulator import Simulator
from migselsim.log import logger

class Run(CommandPlugin):
    """Run simulations."""

    key = 'run'
    description = 'run simulations'
    # registering command line arguments/options has to occur exactly once per
    # class.  This can be most easily achieved at the time the class definition
    # is first read by python interpreter.  Hence, the code is here and not in
    # any class or instance method.
    subparser = command_parsers.add_parser(key, help = 'description')
    subparser.add_argument('conffile', nargs = '?')
    cp.scan()

    @classmethod
    def execute(cls, args):
        conffile = args.conffile

        # When no conffile is supplied, print usage and exit.
        if conffile is None:
            parser.parse_args([cls.key, '--help'])

        # if conffile is not file, print error message and exit.
        if not os.path.isfile(conffile):
            logger.error('File not found: `{}`'.format(conffile))
            return

        try:
            # start reading file.
            with open(conffile, 'r') as f:
                simulators = []
                for model in Model(f, 'xml'):
                    simulators.append(Simulator(model))
        except Exception as e:
            logger.error(e)
            return

        try:
            for simulator in simulators:
                simulator.run()
        except Exception as e:
            logger.error(e)
