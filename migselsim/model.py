# -*- mode: python; coding: utf-8; -*-

from migselsim.definition import MALE, FEMALE, PER_PLOIDY, \
    ALL_AVAIL, NO_STRUCTURE, PROB_OF_MALES, MITOCHONDRIAL


class Model(object):
    """Convert underlying demographic parameters to usable form in simuPOP simulator"""

    def __init__(self, tree):
        self.tree = tree
        self.pop = self._setPopulation()


    def initOps(self):
        """Set up and return operators, which are performed at the beginning of a simulation."""
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
        lineage = sim.InitLineage(lineage = range(1, 2 * sum(pop_size) + 1),
                                  mode = PER_PLOIDY)

        # combine all initializers
        ops.extend(prop)
        ops.extend(geno)
        ops.append(lineage)
        return ops


    def preOps(self):
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
        return ops


    def matingScheme(self):
        tree = self.tree
        pop = self.pop

        numOffspring = tree.get('number of offspring per mating')[0]
        pop_size = tree.get('population size')
        sex_ratio = tree.get('proportion of male')[0]
        mating_mode = tree.get('mating:mode')[0]
        if mating_mode == 'exact':
            sex_mode = (PROB_OF_MALES, sex_ratio)
        else:
            raise Error


        # construct a list for ops parameter in RandomMating.
        # 1. Set MendelianGenoTransmitter() all the time.  This acts
        # as a fall-back transmitter for non-mitochondrial chromosomes
        # when no recombination is specified on them.
        ops = [MendelianGenoTransmitter()]
        # 2. If there is mitochondrial chromosome, we need to specify
        # MitochondrialGenoTransmitter for the chromosome.
        chromTypes = pop.chromTypes()
        if MITOCHONDRIAL in chromTypes:
            ops.append(MitochondrialGenoTransmitter(
                    chroms=[i for i, j in enumearete(chromTypes) if j == MITOCHONDRIAL]))
        # 3. Build *separete* Recombinator for each virtual
        # subpopulation if neccessary.  Similar to selection, it is
        # necessary that each (virtual) subpopulation corresponds to
        # only one Recombinator.
        recs = tree.get('chromosomes:recombination')
        recs_dict = {}
        for r in recs:
            subPops = tuple(subPops)
            if subPops in recs_dict:
                recs_dict[subPops].append(r)
            else:
                recs_dict[subPops] = [r]

        # 2.a convert positions of loci into absolute index, and set
        # up Recombinators.
        ops = [sim.Recombinator(rate = [r.val for r in r_list],
                                loci = [pop.absLocusIndex(r.chrom, r.loci) for r in r_list],
                                subPops = r[0].subPops)
         for r_list in recs_dict.iteritems()]

        return sim.RandomMating(subPopSize = pop_size,
                                sexMode = sex_mode,
                                ops = ops)


    def postOps(self):
        pop = self.pop
        pop_size = sum(self.tree.get('population size'))
        ops = []
        # renumber lineage ids, thereby lineage information refers to unique chromosome
        # in the current generation.
        ops.append(sim.InitLineage(lineage = range(1, 2 * pop_size + 1),
                                  mode = PER_PLOIDY))
        return ops


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
