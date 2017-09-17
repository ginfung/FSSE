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
from Benchmarks.SPL import DimacsModel
from Algorithms.sway_sampler import sway, cont_dominate
from gmpy2 import popcount, mpz
from functools import partial
from repeats import request_new_file
import random
import time
import copy
import pycosat
import pdb


def count1(decint):
    return popcount(mpz(decint))


def split_products(pop, groupC=5):
    rand = random.choice(pop)
    center = count1(int(rand, 2))

    workloads = list()
    dists = list()
    for p in pop:
        wl = count1(int(p, 2))
        dist = count1(wl ^ center)
        workloads.append(wl)
        dists.append(dist)

    poptuple = [(p, i, j) for p, i, j in zip(pop, workloads, dists)]

    # sort by the workloads
    poptuple = sorted(poptuple, key=lambda i: i[1])

    n = int(len(poptuple) / groupC)
    groups = [poptuple[i * n:i * n + n] for i in range(groupC)]

    west, east, westItems, eastItems = list(), list(), list(), list()

    for g in groups:
        k = sorted(g, key=lambda i: i[2])

        # filling the answers
        west.append(k[0][0])
        east.append(k[-1][0])
        westItems.extend(map(lambda i: i[0], k[:len(k) // 2]))
        eastItems.extend(map(lambda i: i[0], k[len(k) // 2:]))

    return west, east, westItems, eastItems


def comparing(part1, part2):
    onewin = 0
    twowin = 0

    for i, j in zip(part1, part2):
        if cont_dominate(i, j) > 0:
            onewin += 1
        else:
            twowin += 1

    return onewin >= twowin


def sat_gen_valid_pop(fm, n):
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
    random.shuffle(pops)
    return pops


def get_sway_res(model):
    # load the  10k sat solutions
    with open('./tse_rs/' + model.name + '.txt', 'r') as f:
        candidates = list()
        for l in f:
            can = model.Individual(l.strip('\n'))
            candidates.append(can)

    # candidates = sat_gen_valid_pop(model, 10000)
    res = sway(candidates, model.eval, partial(split_products, groupC=min(15, model.featureNum // 7)), comparing)
    return res


if __name__ == '__main__':
    # models = ['eshop']
    models = [ 'fiasco', 'freebsd', 'linux']
    for repeat in range(5):
        for name in models:
            print(name)
            model = DimacsModel(name)
            start_time = time.time()
            res = get_sway_res(model)
            finish_time = time.time()
            # save the results
            with open(request_new_file('./tse_rs/sway', name), 'w') as f:
                f.write('T:' + str(start_time) + '\n~~~\n')
                f.write('T:' + str(finish_time) + '\n')
                for i in res:
                    f.write(' '.join(map(str, i.fitness.values)))
                    f.write('\n')
