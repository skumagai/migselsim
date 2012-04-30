# -*- mode: python; coding: utf-8; -*-
from argparse import ArgumentParser

parser = ArgumentParser(usage = '%(prog)s [options] <command> ...')
command_parsers = parser.add_subparsers(title = 'available commands',
                                        dest = 'command')
