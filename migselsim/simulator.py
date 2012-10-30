# -*- mode: python; coding: utf-8; -*-

"""Encapsulate simuPOP individual, population, and simulator classes."""

from migselsim.definition import simuPOP as sim

class Simulator(object):
    """Manage and run actual simulations."""

    def __init__(self, tree):
        self.modle = model(tree)
        self.sim = sim.Simulator(pops = model.pop)


    def run(self):
        """Run simulations"""
        model = self.model
        self.sim.evolve(initOps = model.initOps(),
                        preOps = model.preOps(),
                        matingScheme = model.matingScheme(),
                        postOps = model.postOps())
