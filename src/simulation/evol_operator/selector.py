# -*- mode: python; coding: utf-8; -*-

# selector.py - brief description

# Copyright (C) 2011 Seiji Kumagai <seiji.kumagai@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import simuPOP as sim

from simulation import AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIA

class SelectorProvider(object):
    """Generate selection scheme for given set of incompatibility factors.
    """

    def __init__(self, pop, factors, factor_pos, female_sel, male_sel):
        """Initialize object

        Arguments:
        pop: popluation object
        factors: list of factors
        factor_pos: list of locations of gene within a chromosome
        female_sel: list of selection coefficient of females
                    corresponding to each factor
        male_sel: list of selection coefficient of males
                  corresponding to each factor
        """
        self._pop = pop
        self._factors = factors
        self._factor_pos = factor_pos
        self._female_sel = female_sel
        self._male_sel = male_sel

    def setSelector(self):
        """Prepare selection schemes"""
        sel = {'male':[[], []],
               'female':[[], []]}
        # Position of incompatibility factor

        factors = self._factors
        female_sel = self._female_sel
        male_sel = self._male_sel

        if factors is not None:
            for index, f in enumerate(factors):
                pos = self._pop.absLocusIndex(f, self._factor_pos[index])
                if f == AUTOSOME:
                    ms = self.get2ChromsSelectionMaps(male_sel[index])
                    fs = self.get2ChromsSelectionMaps(female_sel[index])
                    for i in range(2):
                        # For males
                        sel['male'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = ms[i],
                                subPops = [(i, 0)]))
                        # For females
                        sel['female'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = fs[i],
                                subPops = [(i, 1)]))
                elif f == CHROMOSOME_X:
                    ms = self.get1ChromSelectionMaps(male_sel[index])
                    fs = self.get2ChromsSelectionMaps(female_sel[index])
                    for i in range(2):
                        # For males
                        sel['male'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = ms[i],
                                subPops = [(i, 0)]))
                        # For females
                        sel['female'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = fs[i],
                                subPops = [(i, 1)]))
                elif f == CHROMOSOME_Y:
                    ms = self.get1ChromSelectionMaps(male_sel[index])
                    for i in range(2):
                        # Males only
                        sel['male'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = ms[i],
                                subPops = [(i, 0)]))
                else:
                    # Mitochondria
                    # Due to internal design of simuPOP, mitochondria
                    # is considered to be of the type CUSTOMIZED.
                    # This type does not explicitly desiable the
                    # second chromosome.  This requires us to make
                    # explicit mapping of genotype with two
                    # chromosomes to fitness.
                    ms = self.getMtSelectionMaps(male_sel[index])
                    fs = self.getMtSelectionMaps(female_sel[index])
                    for i in range(2):
                        # For males
                        sel['male'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = ms[i],
                            subPops = [(i, 0)])),
                        # For females
                        sel['female'][i].append(sim.MapSelector(
                                loci = pos,
                                fitness = fs[i],
                                subPops = [(i, 1)]))

            # Combine selectors for each factor.
            return [sim.MlSelector(ops = sel[sex][i],
                                   mode = sim.MULTIPLICATIVE,
                                   subPops = [(i, h)])
                    for h, sex in enumerate(['male', 'female']) # Sex
                    for i in range(2)
                    if len(sel[sex][i]) != 0]     # Subpopulations
        else:
            return []


    def get2ChromsSelectionMaps(self, sel):
        """Generate dict of genotype and selection coefficient
        for paird chromosomes.

        This method generates a mapping from genotype with a pair of
        chromosomes to per-locus fitness, and this is used for
        autosomal incompatibility factors for both sex and X-linked
        incompatbility factors for female.

        Arguments:
        sel: selection coefficient
        """
        # In the first deme (deme 0), "0" is the local allele, and "1"
        # is the local allele in the second deme.

        # The first two elements in the following lists are dicts of
        # fitness of genotypes in case of two chromosome.  The rest is
        # in the case of one chromosome (chromosome Y).
        return [{(0, 0): 1.0,
                 (0, 1): sel,
                 (1, 1): sel**2},
                {(0, 0): sel**2,
                 (0, 1): sel,
                 (1, 1): 1.0}]

    def get1ChromSelectionMaps(self, sel):
        """Generate dict of genotype and selection coefficient
        for non-paird chromosomes.

        This method maps single-chromosomal genotype associated with
        X-linked incompatibility factors in males and Y-linked
        incompatibility factors to per-locus fitness.
        Arguments:
        sel: selection coefficient
        """

        return [{(0,): 1.0,
                 (1,): sel},
                {(0,): sel,
                 (1,): 1.0}]

    def getMtSelectionMaps(self, sel):
        """Generate dict of genotype and selection coefficient
        for mitochondria.

        This method maps mitochondrial genotype of incompatibility
        factors to per-locus fitness.  Becasue of simuPOP' design,
        mitochondrial genotypes need to be handled separately.
        Arguments:
        sel: selection coefficient
        """
        # (1, 1) is for placeholder, because MapSelector comlaining
        # missing (1, 1).
        return [{(0, 0): 1.0,
                 (0, 1): sel,
                 (1, 1): -1.0},
                {(0, 0): sel,
                 (0, 1): 1.0,
                 (1, 1): -1.0}]

