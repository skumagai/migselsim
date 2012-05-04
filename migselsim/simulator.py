# -*- mode: python; coding: utf-8; -*-

"""Encapsulate simuPOP individual, population, and simulator classes."""

from migselsim.definition import simuPOP as sim
from migselsim.definition import MALE, FEMALE


class Simulator(object):
    """Manage and run actual simulations."""

    def __init__(self):
        pass

    def run(self):
        # initialize population with given information.
        pop = sim.Population(size = self.population_size,
                             ploidy = self.ploidy,
                             loci = self.loci,
                             chromTypes = self.chromTypes,
                             chromNames = self.chromNames,
                             subPopNames = self.subPopNames,
                             # use for natural selection.
                             infoFields = ['fitness'])
        # set sexes as virtual subpopulations.
        pop.setVirtualSplitter(sim.SexSplitter())

        initOps = self.initOps()
        preOps = self.preOps()
        postOps = self.postOps()
        matingScheme = self.matingScheme()

        simu = sim.Simulator(pop, rep = self.number_of_replicates)

        # now perform simulations
        simu.evolve(initOps = initOps,
                    preOps = preOps,
                    matingScheme = matingScheme,
                    postOps = postOps)

    def initOps(self):
        """Set up operations, which are performed at the beginning of a simulation."""
        # set sex for each deme separately so that sex ratio of demes are roughly identical.
        deme_ids = range(len(self.population_size))
        prop = [sim.InitSex(prop = self.prop, subPops = [i]) for i in deme_ids]
        geno = [sim.InitGenotype(freq = [X, Y] subPops = [(i, sex)])
                for i in deme_ids,
                for sex in [MALE, FEMALE]]
        # combine two groups of initializers
        prop.extend(gene)
        return prop

    def preOps(self):
        pass

    def postOps(self):
        pass

    def matingScheme(self):
        pass
