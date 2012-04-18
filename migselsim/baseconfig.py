# -*- mode: python; coding: utf-8; -*-

"""Handle top-level directive in a config file.

For each directive, a corresponding action is dispatched.
Then each action takes care of inner level directive.

There are currently three top-level directives:

1. genetic structure
2. population structure
3. number of replicates
"""

import yaml
from migselsim.configs import actions

__all__ = ['parse_config']


def parse_config(stream):
    """Parse a YAML-formated configuration file, and apply appropriate settings."""
    data = yaml.load_all(stream)
    for datum in data:
        for item in datum.iteritems():
            key, value = item
            actions[key].main(value, None)
