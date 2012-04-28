# -*- mode: python; coding: utf-8; -*-

import sys
from argparse imort ArgumentParser

from migselsim.commands import CommandPlugin
from migselsim.configs import parse_config
from migselsim.definition import COMMAND

class Run(CommandPlugin):
    """Run simulations."""

    name = 'run'
    description = 'run simulations'
    usage = '{} {} CONFFILE'

    def __init__(self):
        self.parser = ArgumentParser(usage = self.usage.format(COMMAND, self.name))


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
