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
from deap.tools import emo
from Benchmarks.SPL import DimacsModel
from repeats import request_new_file
from operator import itemgetter
from itertools import groupby
import pycosat
import random
import os
import copy
import time
import pdb
import debug

"""
Evaluating all 10k SAT solver results, then use nsga-ii sorting to get the frontier
"""


def action(fm):
    # get the 10k sat solutions
    def sat_gen_valid_pop(n):
        pops = list()
        cnf = copy.deepcopy(fm.cnfs)
        while len(pops) < n:
            for index, sol in enumerate(pycosat.itersolve(cnf)):
                new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
                pops.append(new_ind)
                if index > 20:
                    break
            for x in cnf:
                random.shuffle(x)
            random.shuffle(cnf)

        # for c in range(n):
        #     if c % 1 == 0: print(c)
        #     for sol in pycosat.itersolve(cnf):
        #         new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
        #         print 'x'
        #
        #     sol = pycosat.solve(cnf, vars=fm.featureNum)
        #     # ground_sol = copy.deepcopy(sol)
        #     if isinstance(sol, list):
        #         new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
        #         pops.append(new_ind)
        #         cnf.append([-x for x in sol])
        #         if c % 100 == 0:
        #             for x in cnf:
        #                 random.shuffle(x)
        #             random.shuffle(cnf)
        #     else:
        #         break
        random.shuffle(pops)
        return pops

    start_time = time.time()
    print('start gen ' + fm.name)
    pops = sat_gen_valid_pop(10000)
    print('finish gen ' + fm.name)
    candidates = [fm.Individual(i) for i in pops]

    # pdb.set_trace()
    # with open('/Users/jianfeng/Desktop/tse_rs/' + fm.name + '.txt', 'r') as f:
    #     for l in f:
    #         can = fm.Individual(l.strip('\n'))
    #         candidates.append(can)
    # evaluate all
    for can in candidates:
        fm.eval(can)

    res = emo.sortNondominated(candidates, len(candidates), True)
    finish_time = time.time()

    with open(request_new_file('./tse_rs/god', fm.name), 'w') as f:
        f.write('T:' + str(start_time) + '\n~~~\n')
        f.write('T:' + str(finish_time) + '\n')
        for front in res[0]:
            f.write(' '.join(map(str, front.fitness.values)))
            f.write('\n')

        f.write('~~~\n')


if __name__ == '__main__':
    for repeat in range(1):
        models = ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']
        # models = ['eshop']
        for name in models:
            model = DimacsModel(name)
            action(model)
            print(name)
