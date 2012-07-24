# -*- mode: python; coding: utf-8; -*-

import collections, os

import yaml

from migselsim.baseplugin import PluginMount, Plugin
from migselsim.configs.exceptions import InvalidNodePositionError, DuplicateNodeError, KeyConflictError

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
            raise InvalidNodePositionError(node.id, node.parent)
        root = node.root()
        if cls.conflict != None:
            root = node.root()
            conflicts = [node.find(id_) for id_ in cls.conflict]
            if not all([conf == None for conf in conflicts]):
                raise KeyConflictError(node.id, cls.conflicts)


class Node(object):
    """Node of configuration options."""
    def __init__(self, id_, parent):
        self._id = id_
        self._parent = parent
        self._children = []


    def get(self, key):
        """Obtain value of in descendents of a current node with node with right id.

        If more than one descendent nodes have term as their IDs, a list of values of such
        nodes is returned.  Otherwise, return a single value."""
        # first find a node or nodes with appropriate names.
        # then convert/cast the value into directly usable format by
        # calling convert() method of each associated recipe.

        while key.find(':') > -1:
            if key in ConfigRecipe.plugins:
                okey = key.split(':', 1)[0]
                hits = [ConfigRecipe.plugins[key].apply(node) for node in self.descendents()
                        if node.id == okey]
            else:
                key, rest = key.split(':', 1)
                hits = [node.get(rest) for node in self.descendents() if node.id == key]
            return list(flatten(hits))

        hits = [node for node in self.descendents() if node.id == key]
        if key in ConfigRecipe.plugins:
            values = [ConfigRecipe.plugins[key].apply(node) for node in hits]
        else:
            values = [node.value for node in hits]

        return list(flatten(values))

    def addChild(self, child):
        """Add reference to a child node."""
        self.children.append(child)

    @property
    def children(self):
        """return a list of all children."""
        return self._children

    @property
    def id(self):
        """return a name of current node."""
        return self._id

    @property
    def parent(self):
        """return a parental node."""
        return self._parent

    def root(self):
        """return a root node of a tree."""
        root = self.parent
        while root.parent != None:
            root = root.parent
        return root

    def allNodes(self):
        """return a list of all nodes in a tree."""
        root = self.root()
        return [root] + root.descendents()

    def ancestors(self):
        """return a list of all ancestors."""
        parent = self.parent
        ancestors = [parent]
        while parent != None:
            ancestores.append(parent.parent)
        return ancestors


    def ancestor(self, id_):
        """return an ancestor with name id_."""
        return self._getNode(id_, self.ancestors())

    def descendents(self):
        """return a list of all descendents."""
        descendents = []
        stack = list(self.children)
        while len(stack) > 0:
            top = stack.pop()
            descendents.append(top)
            stack.extend(top.children)
        return descendents

    def descendent(self, id_):
        """return a descendent with name id_."""
        return self._getNode(id_, self.descendents())

    def siblings(self):
        """return a list of sibling nodes except itself."""
        parent = self.parent
        return [child for child in parent.children if child != self]

    def getValueOf(self, id_):
        """return a value of one of descendent node."""
        return self.descendent(id_).value

    def find(self, id_):
        """find a node with a specific id within a tree."""
        return self._getNode(id_, [self] + node.ancestors + node.descendent)

    def _getNode(self, id_, nodes):
        """find a node with a specific id in a list of nodes, and return the node."""
        node = [n for n in nodes if n.id == id_]
        nnode = len(node)
        if nnode == 1:
            return node[0]
        elif nnode > 1:
            raise DuplicateNodeError(id_)
        else:
            return None




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
