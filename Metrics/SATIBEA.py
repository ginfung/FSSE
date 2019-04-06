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

# cover from http://research.henard.net/SPL/ICSE_2015
# DEAP + MINISAT+ IBEA alg

from Benchmarks.SPL import DimacsModel
from deap import algorithms
from deap import tools
from selIBEA import selIBEA
import time
import pycosat
import copy
import pdb
import os
import random
import debug


def action(fm):
    fm.toolbox.register('select', selIBEA)

    print('start!')

    dead, mandatory = list(), list()

    def prepare():
        global dead, mandatory
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../Benchmarks/dimacs/' + fm.name + '.dimacs.dead',
                  'r') as f:
            dead = f.readlines()
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../Benchmarks/dimacs/' + fm.name + '.dimacs.mandatory',
                  'r') as f:
            mandatory = f.readlines()
        dead = map(lambda i: int(i[:-1]) - 1, dead)
        mandatory = map(lambda i: int(i[:-1]) - 1, mandatory)

    def sat_gen_valid_pop(n):
        pops = list()
        cnf = copy.deepcopy(fm.cnfs)
        for c in range(n):
            print(c)
            sol = pycosat.solve(cnf, vars=fm.featureNum)
            # ground_sol = copy.deepcopy(sol)
            if isinstance(sol, list):
                new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
                pops.append(new_ind)
                cnf.append([-x for x in sol])
                for x in cnf:
                    random.shuffle(x)
                random.shuffle(cnf)
            else:
                break
        return pops

    def sat_ibea_mutate(ind):
        # ICSE 2015 mutate settings
        decs = [i for i in ind]
        if random.random() < 0.98:
            # apply standard mutation
            for x in range(len(decs)):
                if random.random() < 0.001 and x not in dead and x not in mandatory:
                    decs[x] = str(1 - int(decs[x]))
        else:
            if random.random() < 0.5:
                # apply smart mutation
                for x in range(len(decs)):
                    if random.random() < 0.001 and x not in dead and x not in mandatory:
                        decs[x] = str(1 - int(decs[x]))

                false_list = list()
                for c_i, c in enumerate(fm.cnfs):
                    corr = False
                    for x in c:
                        if (x > 0 and decs[abs(x) - 1] == '1') or (x < 0 and decs[abs(x) - 1] == '0'):
                            corr = True
                            break
                    if not corr:
                        false_list.extend([abs(x) for x in c])

                if len(false_list) > 0:
                    cnf = copy.deepcopy(fm.cnfs)
                    for i, v in enumerate(decs):
                        if i in false_list: continue
                        if v == '1':
                            cnf.append([i + 1])
                        else:
                            cnf.append([-i - 1])
                    for x in cnf: random.shuffle(x)
                    random.shuffle(cnf)
                    sol = pycosat.solve(cnf, vars=fm.featureNum)
                    if sol != 'UNSAT':
                        new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
                        return new_ind,
            else:
                # apply smart replacement
                cnf = copy.deepcopy(fm.cnfs)
                for x in cnf: random.shuffle(x)
                random.shuffle(cnf)
                sol = pycosat.solve(cnf, vars=fm.featureNum)
                if sol != 'UNSAT':
                    new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
                    return new_ind,

        return fm.Individual(''.join(decs)),

    def sat_ibea_cx(ind1, ind2):
        dec1 = [i for i in ind1]
        dec2 = [i for i in ind2]
        break_point = random.randint(1, len(dec1) - 1)
        for i in range(len(dec1)):
            if i > break_point: break
            dec1[i], dec2[i] = dec2[i], dec1[i]
        return fm.Individual(''.join(dec1)), fm.Individual(''.join(dec2))

    fm.toolbox.register('mutate', sat_ibea_mutate)
    fm.toolbox.register('mate', sat_ibea_cx)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)

    global last_save_time
    last_save_time = time.time()

    def save_all_pop_fitness(source):
        global last_save_time
        if time.time() - last_save_time > 15:  # save the pop every 15 seconds
            last_save_time = time.time()
            return source
        else:
            return 'pass'

    def save_time(source):
        return time.time()

    prepare()

    stats.register('time', save_time)
    stats.register('fitness', save_all_pop_fitness)

    pop = sat_gen_valid_pop(300)
    for p in pop: fm.eval(p)
    res = algorithms.eaMuPlusLambda(
        population=pop,
        toolbox=fm.toolbox,
        mu=300,
        lambda_=300,
        cxpb=0.05,
        mutpb=0.95,
        ngen=50,
        stats=stats
    )

    return res