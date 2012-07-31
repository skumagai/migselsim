# -*- mode: python; coding: utf-8; -*-

import collections, os

import yaml

from migselsim.baseplugin import PluginMount, Plugin
from migselsim.configs.exceptions import WrongPosition, NodeRepeated, ConflictingNodes
from migselsim.configs.node import Node

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

    :apply: an entry point to configure a simulator.  Takes instances of node and simulator
    classes.

    """
    __metaclass__ = ConfigPluginMount

    @classmethod
    def apply(cls, node):
        NotImplementedError

    @classmethod
    def validate(cls, node):
        if node.parent.id != cls.parent:
            raise WrontPosition
        root = node.root()
        if cls.conflict != None:
            root = node.root()
            conflicts = [node.find(id_) for id_ in cls.conflict]
            if not all([conf == None for conf in conflicts]):
                raise ConflictingNodes



def parse_config(stream):
    """Parse a YAML-formated configuration file and return tree of configuration options."""
    data = yaml.load_all(stream)
    return [build_tree(datum) for datum in data]

def build_tree(data):
    """Construct tree of configuration options from YAML-formatted input."""
    tree = construct_node('root', data, None)
    return tree

def construct_node(id_, data, parent):
    """Recursively build a node representing configuration option."""
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


# Auxilliary functions to debug config tree.
def print_tree(node):
    """Pretty print a tree with a given node as a root."""
    print_node(node, 0)


def print_node(node, level):
    """Print an ID of node with an appropriate indentation, then recursively print children."""
    print ' ' * 2 * level + '-' +  node.id
    for child in node.children:
        print_node(child, level + 1)


def flatten(l):
    """flatten list of arbitrary depth.

    Authored by cristian at stackoverflow.com (http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python)
    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
