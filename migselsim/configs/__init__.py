# -*- mode: python; coding: utf-8; -*-

import os
import sys

import yaml

from migselsim.baseplugin import PluginMount, Plugin
from migselsim.simulator import Simulator
from migselsim.exception import WrongConfigParentError

# Register config plugins by scanning the directory and import all modules.
# Imported plugins are normal python file (*.py), and their names need not
# start with '__' such as (__init__.py).

class ConfigPluginMount(PluginMount):
    """
    Parental class of all config plugins.

    All plugins inherited from this class are registered in ConfigPluginMount dict.
    """
    pass


class ConfigRecipe(Plugin):
    """
    Configure simulator given a node of configuration tree.

    Any class implementing this interface should provide the following attributes:

    :key: Name of configuration key.

    :child: List of names of child nodes.  Terminal nodes take None for this variable.  Used for validation.

    :parent: Name of parental node.  Root node takes None for this variable.  Used for validation.

    :conflict: List of names of conflicting config nodes.  Two nodes are in conflict when
    two nodes specify the same aspect of simulations.

    """
    __metaclass__ = ConfigPluginMount

    def get(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            for child in self.child:
                if child.key == key:
                    return child
                else:
                    raise IndexError

class Node(object):
    """Node of configuration options."""
    def __init__(self, id_, parent):
        self.id = id_
        self.parent = parent
        self.children = []


    def addChild(self, child):
        """Add reference to a child node."""
        self.children.append(child)

    def getChildren(self):
        return self.children


def parse_config(stream):
    """Parse a YAML-formated configuration file and return tree of configuration options."""
    data = yaml.load_all(stream)
    return [build_tree(datum) for datum in data]

def build_tree(data):
    """Construct tree of configuration options from YAML-formatted input."""
    tree = construct_node('root', data, None)
    return tree

def construct_node(id_, data, parent):
    node = Node(id_, parent)
    dtype = type(data)
    if dtype == list:
        for subid_, value in enumerate(data):
            node.addChild(construct_node(id_ + str(subid_), value, node))
    elif dtype == dict:
        for key, value in data.iteritems():
            node.addChild(construct_node(key, value, node))
    else:
        # If data is atomic, the node is terminal (without any
        # children).
        node.value = data

    return node

def setup_simulator(config):
    sim = Simulator()



# Auxilliary functions to debug config tree.
def print_tree(node):
    """Pretty print a tree with a given node as a root."""
    print_node(node, 0)


def print_node(node, level):
    """Print an ID of node with an appropriate indentation, then recursively print children."""
    print ' ' * 2 * level + '-' +  node.id
    for child in node.getChildren():
        print_node(child, level + 1)

    # ConfigNode.scan()
    #     # sim = Simulator()
    #     # simulators.append(sim)
    # return simulators

# Scan plugin directory when this file is loaded.
ConfigRecipe.scan()
