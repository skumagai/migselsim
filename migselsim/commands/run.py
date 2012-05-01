# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import CommandPlugin
from migselsim.configs import parse_config
from migselsim.log import logger

class Run(CommandPlugin):
    """Run simulations."""

    key = 'run'
    description = 'run simulations'
    usage = '{} {} CONFFILE'

    def execute(self, options, args):

        if len(args) == 1:
            self.parser.print_help()
            return

        # parse config and set up simulator
        simulators = None
        with open(args[2], 'r') as f:
            simulators = parse_config(f)

        # perform simulations
        for simulator in simulators:
            simulator.run()
