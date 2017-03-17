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
from deap.tools.emo import sortNondominated
from deap import creator, base
from repeats import fetch_all_files
import os
import pdb

"""
The the union of all solutions and fetch the frontier
"""


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

folders = [
    '/Users/jianfeng/Desktop/tse_rs/god/',
    '/Users/jianfeng/Desktop/tse_rs/sway/',
]

# models = ['osp', 'osp2', 'ground', 'flight']
models = ['p3a', 'p3b', 'p3c']
union_candidates = list()

creator.create("FitnessMin", base.Fitness, weights=[-1.0] * 3)  # TODO set "4"?
creator.create("Individual", str, fitness=creator.FitnessMin)

for model in models:
    union_candidates = []
    for f in folders:
        for i in fetch_all_files(f, model):
            with open(i, 'r') as records:
                content = records.readlines()
            content = map(lambda l: l.strip('\n'), content)
            for l in content:
                if l.startswith('T') or l.startswith('~~~') or l.startswith('G'):
                    continue
                e = l.split(' ')
                e = [float(i) for i in e]
                ind = creator.Individual(str(e))
                ind.fitness = creator.FitnessMin(e)

                union_candidates.append(ind)
    # pdb.set_trace()
    frontier = _get_frontier(union_candidates)

    # write out the frontier
    with open(os.path.dirname(os.path.abspath(__file__))+'/'+model+'.txt', 'w') as f:
        for front in frontier:
            f.write(' '.join(map(str, front.fitness.values)))
            f.write('\n')
