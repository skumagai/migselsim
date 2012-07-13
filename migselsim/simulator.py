# -*- mode: python; coding: utf-8; -*-

"""Encapsulate simuPOP individual, population, and simulator classes."""

from migselsim.definition import simuPOP as sim
from migselsim.definition import MALE, FEMALE, PER_PLOIDY, ALL_AVAIL, NO_STRUCTURE

class Simulator(object):
    """Manage and run actual simulations."""

    def __init__(self, tree):
        self.tree = tree
        # initialize population with given information.
        self._setPopulation()
        self.sim = sim.Simulator(self.pop)
        self._setInitOps()
        self._setPreOps()
        self._setPostOps()
        self._setMatingScheme()

    def _setPopulation(self):
        """configure attributes of a population from a tree of configuration options."""
        tree = self.tree
        size = tree.get('population size')
        loci = tree.get('number of loci')
        chromTypes = tree.get('chromosome types')
        chromNames = tree.get('chromosome ids')
        subPopNames = tree.get('subpopulation name')
        self.pop = sim.Population(size = size,
                                  ploidy = 2,
                                  loci = loci,
                                  chromTypes = chromTypes,
                                  subPopNames = subPopNames,
                                  infoFields = ['fitness', 'migrate_to'])
        self.pop.setVirtualSplitter(sim.SexSplitter())




    def run(self):
        """Run simulations"""
        self.sim.evolve(initOps = self.initOps,
                        preOps = self.preOps,
                        matingScheme = self.matingScheme,
                        postOps = self.postOps)

    def initOps(self):
        """Set up operations, which are performed at the beginning of a simulation."""
        # set sex for each deme separately so that sex ratio of demes
        # are roughly identical.
        pop = self.pop
        tree =self.tree
        pop_size = tree.get("population size")
        male_prop = tree.get("proportion of male")
        non_neutral_loci = tree.get("non-neutral loci")

        ops = []
        prop = [sim.InitSex(maleProp = male_prop, subPops = [i]) for i in range(len(pop_size))]

        # Initialize genotype sex-by-sex and deme-by-deme basis.
        # This could be highly more efficient but it's not worth it,
        # as they are called only once at the beginning of a
        # simulation.
        try:
            geno = [_construct_genotype(locus) for locus in self.non_neutral_loci]
        except:
            geno = []

        # Initialize lineage.  All genes on the first set of chromosomes have the same id.
        # Similarly, all genes on the second set of chromosomes have the same id.
        # However, these ids are different between the first and second sets of chromosomes.
        # This scheme can be specified as mode = PER_PLOIDY in simuPop.InitLineage.
        lineage = sim.InitLineage(lineage = range(2 * sum(self.population_size)),
                                  mode = PER_PLOIDY)

        # combine all initializers
        ops.extend(prop)
        ops.extend(geno)
        ops.append(lineage)
        return ops

    def preOps(self):
        pop = self.pop
        ops = []
        # selection
        try:
            # If there is at least one locus that is under sex- or
            # deme-specific selection, there should be enough number
            # of separate MlSelectors.
            # For example, suppose there are three demes, and
            # selection is deme-specific but not sex-specific.  Then,
            # we need three MlSelectors.
            # If selection is also sex-specific, we need 6 selectors.

            # Find if selection is deme-specific (in at least one deme).
            deme_specific = any(NO_STRUCTURE != locus['deme'] for locus in self.non_neutral_loci)

            # Find if selection is sex-specific.
            sex_specific = any(NO_STRUCTURE != locus['sex'] for locus in self.non_neutral_loci)

            if deme_specific or sex_specific:
                sel = [sim.MlSelector(
                        ops = [sim.MapSelector(loci = pop.absLocusIndex(locus['chromosome'],
                                                                        locus['position']),
                                               fitness = locus['coeff'],
                                               subPops = [_form_subdeme(locus['deme'],
                                                                        locus['sex'])])
                               for locus in self.non_neutral_loci],
                        mode=MULTIPLICATIVE)]
        except:
            sel = []


        # migration
        try:
            if self.migration[0]['sex'] == ALL_AVAIL:
                # sex-nonspecific migration, and length of self.migration
                # is 1.
                mig = self.migration[0]
                migs = [sim.Migrator(rate = mig['matrix'],
                                     mode = mig['type'])]
            else:
                # sex-specific migration
                npop = len(sim.population_size)
                mig = [sim.Migrator(rate = mig['matrix'][sex],
                                    mode = mig['type'],
                                    subPops = [(deme, vidx) for deme in range(npop)])
                       for (sex, vidx) in zip(['male', 'female'], [0,1])]
        except:
            # no migration.
            mig = []

        # combine all premating operations
        ops.extend(sel)
        ops.extend(mig)
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
        recs = sim.Recombinator()
        return sim.RandomMating(ops = recs)


def _construct_genotype(locus):
    # subPops need to be constructed before passing to InitGenotype,
    # because specifial handling is required when no sex- and deme
    # specificity is required.
    prop = locus['prop']
    loci = pop.absLocusIndex(locus['chromosome'], locus['position'])
    deme = locus['deme']
    sex = locus['sex']
    if deme == NO_STRUCTURE and sex == NO_STRUCTURE:
        return sim.InitGenotype(prop = prop, loci = loci)
    # elif deme == NO_STRUCTURE:
    #     all_demes = range(len(self.population_size))
    #     return sim.InitGenotype(prop = prop, loci = loci,
    #                        subPops = [_form_subdeme(deme, sex) for deme in all_demes])
    # elif sex == NO_STRUCTURE:
    #     all_demes = range(len(self.population_size))
    #     return sim.InitGenotype(prop = prop, loci = loci, subPops = all_demes)
    else:
        all_demes = range(len(self.population_size))
        all_vpops = [_form_subdeme(deme, sex) for deme in all_demes]
        return sim.InitGenotype(prop = prop, loci = loci, subPops = all_vpops)

def _form_subdeme(loc, sex):
    """return tuple indicating subdemes.  The size of tuple depends on both deme- and
    sex-specificty of non-neutral loci."""
    if loc != NO_STRUCTURE and sex != NO_STRUCTURE:
        return (loc, sex)
    elif loc != NO_STRUCTURE:
        return (loc)
    elif sex != NO_STRUCTURE:
        return (sex)
    else:
        # should not reach to this branch.
        return ()
