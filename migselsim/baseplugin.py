# -*- mode: python; coding: utf-8; -*-

# simple plugin framework adapted from
# http://martyalchin.com/2008/jan/10/simple-plugin-framework/
# by Marty Alchin

import os
import sys
import pkgutil

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        try:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins[cls.key] = cls
        except AttributeError:
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = {}

    def scan(cls):
        """Scan and load plugins.

        This should be used from within the plugin directory"""
        # urgly hack to get the absolute path of plugin directory.
        plugindir = cls.__module__
        plugindir = os.path.splitext(plugindir)[1][1:]
        topdir = os.path.split( __file__)[0]

        # need to be ta list.
        plugindir = [os.path.join(topdir, plugindir)]
        # TODO: better support multiple plugin directory.
        for dummy, module, dummy in \
                pkgutil.walk_packages(plugindir, cls.__module__ + '.'):
            if not module in sys.modules:
                try:
                    __import__(module)
                except:
                    raise

class Plugin(object):
    """
    Plugin base class.

    This class only defines very basic interface and should not be used directly.
    Rather, plugin systems should subclass this first to define specific plugin
    interface, and then subclass the specific plugin class to define
    concrete plugins.

    :key: command name

    """

    key = None

    # placeholder, should be also use an appropriate subclass of PluginMount.
    __metaclass__ = PluginMount
