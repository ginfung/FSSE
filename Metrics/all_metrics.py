#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


from __future__ import division
from decimal import Decimal
from deap.benchmarks.tools import diversity, convergence
from deap import creator, base
from deap.tools.emo import sortNondominated
from Metrics.hv import HyperVolume
from Metrics.gd import GD
from Metrics.gs import GS
import pdb


def _get_frontier(pop):
    """
    return the pareto frontier of the given pop. No duplicate individuals in the returns
    :param pop:
    :return:
    """
    front = sortNondominated(pop, len(pop), True)[0]
    uniques = []
    for f in front:
        if f not in uniques:
            uniques.append(f)
    return uniques


def put_record_here(filename, model):
    def calc(PFc):
        creator.create("FitnessMin", base.Fitness, weights=[-1.0] * len(PFc[0]))
        creator.create("Individual", str, fitness=creator.FitnessMin)

        pop = list()
        for sol in PFc:
            ind = creator.Individual(str(sol))  # a trick here... use the fitness to identify solutions
            ind.fitness = creator.FitnessMin(sol)
            pop.append(ind)
        del PFc
        PFc = pop[:]
        del pop
        PFc = _get_frontier(PFc)  # DEAP version
        PFc_list = [i.fitness.values for i in PFc]  # PYTHON LIST version

        if len(PFc) < 3:
            return '%s\t%s\t%s\t%s\t%s' % ('n/a', 'n/a', 'n/a', str(len(PFc)), 'n/a'), []

        # GD
        # load the PF0
        PF0 = list()
        with open('./PF_0/' + model + '.txt', 'r') as f:
            for l in f:
                e = l.strip('\n').split(' ')
                e = [float(i) for i in e]
                PF0.append(e)
        gd = GD(PF0, PFc_list)
        # print('GD =GD ', '%.3E'%Decimal(str(gd)))

        # GS
        gs = GS(PF0, PFc_list)
        # print('GS = ', '%.3E'%Decimal(str(gs)))
        # PFS
        pfs = len(PFc)
        # print('PFS = ', str(pfs))
        # HV
        rp = [1] * len(PFc[0].fitness.values)  # reference point

        hv = HyperVolume(rp).compute(PFc_list)
        hv = round(hv, 4)
        # print('HV = ', str(hv))

        return '%s\t%s\t%s\t%s\t%s' % (model, '%.3E' % Decimal(str(gd)), '%.3E' % Decimal(str(gs)), str(pfs), str(hv)), PFc_list

    PFc = list()
    # canNum = 0
    with open(filename, 'r') as f:
        content = f.readlines()
    content = map(lambda l: l.strip('\n'), content)

    times = list()

    PFc = []

    for l in content:
        if l.startswith('T:'):
            times.append(float(l[2:]))
            continue
        if l.startswith('Gen:'):
            continue
        if l.startswith('~~~'):
            if len(PFc):
                mas, saved = calc(PFc)
                print(str(round(times[-1]-times[0], 2)) + '\t' + mas)
                PFc = saved
            continue
        # filtering for SPL
        e = l.split(' ')
        e = [round(float(i), 3) for i in e]
        if e[0] > 0.00001: continue
        PFc.append(e[1:])

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    import debug
    # models = ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']
    models = ['linux']
    for name in models:
        print('MODEL = ', name)
        put_record_here('/Users/jianfeng/Desktop/tse_rs/random/'+name+'.txt', name)
        print('\n\n')
