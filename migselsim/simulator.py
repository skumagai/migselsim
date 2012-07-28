# -*- mode: python; coding: utf-8; -*-

"""Encapsulate simuPOP individual, population, and simulator classes."""

from migselsim.definition import simuPOP as sim
from migselsim.definition import MALE, FEMALE, PER_PLOIDY, ALL_AVAIL, NO_STRUCTURE, PROB_OF_MALES, MITOCHONDRIA

class Simulator(object):
    """Manage and run actual simulations."""

    def __init__(self, tree):
        self.tree = tree
        # initialize population with given information.
        self._setPopulation()
        self._setInitOps()
        self._setPreOps()
        self._setPostOps()
        self._setMatingScheme()
        # self.sim = sim.Simulator(pops = self.pop)

    def _setPopulation(self):
        """configure attributes of a population from a tree of configuration options."""
        tree = self.tree
        size = tree.get('population size')
        print size
        loci = tree.get('number of loci')
        chromTypes = tree.get('chromosomes:type')
        chromNames = tree.get('chromosomes:id')
        self.pop = sim.Population(size = size,
                                  ploidy = 2,
                                  loci = loci,
                                  chromTypes = chromTypes,
                                  chromNames = chromNames,
                                  infoFields = ['fitness', 'migrate_to'])
        self.pop.setVirtualSplitter(sim.SexSplitter())
        print self.pop.chromTypes()
        print (AUTOSOME, CHROMOSOME_X)


    def run(self):
        """Run simulations"""
        pass
        # self.sim.evolve(initOps = self.initOps,
        #                 preOps = self.preOps,
        #                 matingScheme = self.matingScheme,
        #                 postOps = self.postOps)

    def _setInitOps(self):
        """Set up operations, which are performed at the beginning of a simulation."""
        # set sex for each deme separately so that sex ratio of demes
        # are roughly identical.
        pop = self.pop

        tree =self.tree
        pop_size = tree.get("population size")
        male_prop = tree.get("proportion of male")[0]

        ops = []
        # by setting initial proportion of males separetely to each
        # deme, I have finer control of the proportion.  Otherwise,
        # proportion in each population might not exactly be as
        # desired.
        prop = [sim.InitSex(maleProp = male_prop, subPops = [i]) for i in range(len(pop_size))]

        # We only care allele frequencies of non-neutral loci, because
        # we keep track of lineages rather than alleles for neutral
        # loci.
        geno = [sim.InitGenotype(freq  = g.val,
                                 loci = [pop.absLocusIndex(g.chrom, locus)
                                         for locus in g.loci],
                                 subPops = g.subPops)
                for g in tree.get("non-neutral loci:initial frequency")]


        # Initialize lineage.  All genes on the first set of chromosomes have the same id.
        # Similarly, all genes on the second set of chromosomes have the same id.
        # However, these ids are different between the first and second sets of chromosomes.
        # This scheme can be specified as mode = PER_PLOIDY in simuPop.InitLineage.
        lineage = sim.InitLineage(lineage = range(2 * sum(pop_size)),
                                  mode = PER_PLOIDY)

        # combine all initializers
        ops.extend(prop)
        ops.extend(geno)
        ops.append(lineage)
        self.intiOps = ops

    def _setPreOps(self):
        tree = self.tree
        pop = self.pop
        ops = []
        # selection
        # Because MlSelector only works well if all single locus
        # selectors (MapSelector) target to the same
        # populations, I must filter and separete selection schemes by
        # target populations.

        # identify and separate the number of targets population.
        targets = {}
        for s in tree.get('non-neutral loci:selection coefficient'):
            # because list is not hashable, convert deme (originally a
            # list) to tuple.
            deme = tuple(s.subPops)
            if deme not in targets:
                targets[deme] = [s]
            else:
                targets[deme].append(s)

        sel = [sim.MapSelector(loci = pop.absLocusIndex(s[0].chrom, s[0].loci),
                               fitness = s[0].val,
                               subPops = s[0].subPops)
               if len(s) == 1 else
               sim.MlSelector(ops =
                              [sim.MapSelector(loci = pop.absLocusIndex(ss.chrom, ss.loci),
                                               fitness = ss.val,
                                               subPops = ss.subPops)
                               for ss in s],
                              subPops = s[0].subPops)
               for s in targets.itervalues()]

        # migration
        mig = [sim.Migrator(rate = matrix.val)
               for matrix in tree.get('migration:matrix')]

        # combine all premating operations
        ops.extend(sel)
        ops.extend(mig)
        self.preOps = ops


    def _setPostOps(self):
        pop = self.pop
        pop_size = sum(self.tree.get('population size'))
        ops = []
        # renumber lineage ids, thereby lineage information refers to unique chromosome
        # in the current generation.
        ops.append(sim.InitLineage(lineage = range(2 * pop_size),
                                  mode = PER_PLOIDY))
        self.postOps = ops

    def _setMatingScheme(self):
        pop = self.pop
        tree = self.tree

        numOffspring = tree.get('number of offspring per mating')[0]
        pop_size = tree.get('population size')
        sex_ratio = tree.get('proportion of male')[0]
        mating_mode = tree.get('mating:mode')[0]
        if mating_mode == 'exact':
            sex_mode = (PROB_OF_MALES, sex_ratio)
        else:
            raise Error


        # construct a list for ops parameter in RandomMating.
        # 0. Use MendelianGenoTransmitter() all the time.  This works
        # as fall-back transmitter for non-mitochondrial chromosomes
        # when no recombination is specified on some chromosomes.
        ops = [MendelianGenoTransmitter()]
        # 1. If there is mitochondrial chromosome, we need to specify
        # MitochondrialGenoTransmitter for the chromosome.
        chromTypes = pop.chromTypes()
        if MITOCHONDRIAL in chromTypes:
            ops.append(MitochondrialGenoTransmitter(
                    chroms=[i for i, dummy in enumearete(chromTypes) if i == MITOCHONDRIAL]))
        # 2. Build *separete* Recombinator for each virtual
        # subpopulation if neccessary.  Similar to selection, it is
        # necessary that each (virtual) subpopulation corresponds to
        # only one Recombinator.
        # 2.a convert positions of loci into absolute index.
        # recs = tree.get('chromosomes:recombination')
        # pos = [pop.absLocusIndex(rec.chrom, rec.loci) for rec in recs]
        # rates = [rec.val for rec in recs]
        # [sim.Recombinator(rate = rec.val,
        #                   loci = [pop.absLocusIndex(rec.chrom,
        #                                             locus)
        #                           for locus in rec.loci],
        #                   subPops = rec.subPops)
        #  for rec in tree.get('chromosomes:recombination')]


        sim.RandomMating(subPopSize = pop_size,
                         sexMode = sex_mode,
                         ops = ops)
        # recs = sim.Recombinator()
        # return sim.RandomMating(ops = recs)
