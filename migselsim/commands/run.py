# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.commands import CommandPlugin


class Run(CommandPlugin):
    """Run simulations."""

    name = 'run'
    description = 'run simulations'

    def __init__(self):
        self.parser =


    def execute(self, options, args):
