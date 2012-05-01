# -*- mode: python; coding: utf-8; -*-
from argparse import ArgumentParser

parser = ArgumentParser()
command_parsers = parser.add_subparsers(title = 'available commands',
                                        dest = 'command')
