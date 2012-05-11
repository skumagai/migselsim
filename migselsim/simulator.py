# -*- mode: python; coding: utf-8; -*-

"""Encapsulate simuPOP individual, population, and simulator classes."""

from migselsim.definition import simuPOP as sim
from migselsim.definition import MALE, FEMALE, PER_PLOIDY


class Simulator(object):
    """Manage and run actual simulations."""

    def __init__(self):
        pass

    def run(self):
        # initialize population with given information.
        self.pop = sim.Population(size = self.population_size,
                                  ploidy = 2,
                                  loci = self.loci,
                                  chromTypes = self.chromTypes,
                                  chromNames = self.chromNames,
                                  subPopNames = self.subPopNames,
                                  # use for natural selection.
                                  infoFields = ['fitness'])
        # set sexes as virtual subpopulations.
        self.pop.setVirtualSplitter(sim.SexSplitter())

        initOps = self.initOps()
        preOps = self.preOps()
        postOps = self.postOps()
        matingScheme = self.matingScheme()

        simu = sim.Simulator(self.pop, rep = self.number_of_replicates)

        # now perform simulations
        simu.evolve(initOps = initOps,
                    preOps = preOps,
                    matingScheme = matingScheme,
                    postOps = postOps)

    def initOps(self):
        """Set up operations, which are performed at the beginning of a simulation."""
        # set sex for each deme separately so that sex ratio of demes
        # are roughly identical.
        pop = self.pop
        deme_ids = range(len(self.population_size))
        ops = []
        prop = [sim.InitSex(maleProp = self.maleProp, subPops = [i]) for i in deme_ids]

        # Initialize genotype sex-by-sex and deme-by-deme basis.
        # This could be highly more efficient but it's not worth it,
        # as they are called only once at the beginning of a simulation.
        geno = [sim.InitGenotype(prop = locus['prop'],
                                 loci = pop.absLocusIndex(locus['chromsome'],
                                                          locus['position']),
                                 # subPops must be form [[]] (nested sequence).
                                 # Otherwise (deme, sex) pair is interpreted as
                                 # two separate subpopulations: 'deme' and 'sex',
                                 # rather than virtual subpopulations.
                                 subPops = [(locus['deme'],
                                             locus['sex'])])
                for locus in self.non_neutral_loci]

        # Initialize lineage.  All genes on the first set of chromosomes have the same id.
        # Similarly, all genes on the second set of chromosomes have the same id.
        # However, these ids are different between the first and second sets of chromosomes.
        # This scheme can be specified as mode = PER_PLOIDY in simuPop.InitLineage.
        lineage = sim.InitLineage(lineage = range(2 * sum(self.population_size)),
                                  mode = PER_PLOIDY)

        # combine all initializers
        ops.extend(prop)
        ops.extend(gene)
        ops.append(lineage)
        return ops

    def preOps(self):
        pop = self.pop
        ops = []
        # selection
        sel = [sim.MapSelector(loci = pop.absLocusIndex(locus['chromosome'],
                                                        locus['position']),
                               fitness = locus['coeff'],
                               subPops = [(locus['deme'],
                                           locus['sex'])])
                for locus in self.non_neutral_loci]
        # migration
        ops.extend(sel)
        return ops


    def postOps(self):
        pop = self.pop
        ops = []
        # renumber lineage ids, thereby lineage information refers to unique chromosome
        # in the current generation.
        ops.append(sim.InitLineage(lineage = range(2 * sum(self.population_size)),
                                  mode = PER_PLOIDY))
        return ops

    def matingScheme(self):
        pop = self.pop
