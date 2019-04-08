#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, _distribute, sublicense, and/or sell
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

import sys
import os
path = os.getcwd()
rootpath = path[:path.rfind('FSSE') + 4]
sys.path.append(rootpath)

from Algorithms.sway_sampler import sway, bin_dominate, cont_dominate
from Algorithms import NSGA2, WORTHY

from Benchmarks import XOMO, POM3
from deap.tools import emo
import functools
import time
import random


def get_sway_res(model):
    def _dist(ind1, ind2):
        d = 0
        for i, j in zip(ind1, ind2):
            d += (i - j)**2
        return d

    def _where(pop):
        rand = random.choice(pop)
        ds = [_dist(i, rand) for i in pop]
        east = pop[ds.index(max(ds))]
        ds = [_dist(i, east) for i in pop]
        west = pop[ds.index(max(ds))]

        c = _dist(east, west)
        cc = 2 * c**0.5

        mappings = list()
        for x in pop:
            a = _dist(x, west)
            b = _dist(x, east)
            d = (a + c - b) / cc
            mappings.append((x, d))

        mappings = sorted(mappings, key=lambda i: i[1])
        mappings = [i[0] for i in mappings]

        n = len(mappings)
        eastItems = mappings[:int(n * 0.2)] + mappings[int(n * 0.5):int(n *
                                                                        0.8)]
        westItems = mappings[int(n * 0.2):int(n * 0.5)] + mappings[int(n *
                                                                       0.8):]

        # westItems = mappings[len(mappings)//2:]
        return west, east, eastItems, westItems

    def _comparing(part1, part2):
        return bin_dominate(part1, part2)

    # Starting SWAY execution here
    candidates = list()
    for _ in range(10000):
        ran_dec = [random.random() for _ in range(model.decsNum)]
        can = model.Individual(ran_dec)
        candidates.append(can)
    res = sway(candidates, functools.partial(model.eval, normalized=False),
               _where, _comparing)

    return res


def get_random_res(model, size=10000):
    # generating the 10k random solutions
    candidates = list()
    for _ in range(size):
        ran_dec = [random.random() for _ in range(model.decsNum)]
        can = model.Individual(ran_dec)
        candidates.append(can)
    print('random sol created.')
    for can in candidates:
        model.eval(can, normalized=False)
    print('finish evaluating.')
    res = emo.sortNondominated(candidates, len(candidates), True)[0]
    print('finish selection.')
    finish_time = time.time()
    return res


def get_nsga2_res(model):
    return NSGA2.action(model, mu=300, ngen=50, cxpb=0.9, mutpb=0.15)


def get_worthy_res(model):
    return WORTHY.action(model)


"""
python Experiments/main.py
-alg NSGA2/SWAY/RANDOM/WORTHY
-m 0~6
-r 20
"""
if __name__ == '__main__':
    # Parsing the sys.argv
    alg = 'WORTHY'
    model_id = 0
    repeat = 1
    for i, v in enumerate(sys.argv):
        if v == '-alg':
            alg = sys.argv[i + 1]
        if v == '-model':
            model_id = int(sys.argv[i + 1])
        if v == '-r':
            repeat = int(sys.argv[i + 1])

    alg = alg.upper()

    XOMO_OSP, XOMO_OSP2, XOMO_GROUND, XOMO_FLIGHT = XOMO.pre_defined()
    POM3a, POM3b, POM3c = POM3.pre_defined()[:3]
    models = [
        XOMO_OSP, XOMO_OSP2, XOMO_GROUND, XOMO_FLIGHT, POM3a, POM3b, POM3c
    ]
    model = models[model_id]
    # End parsing the sys.argv

    for _ in range(repeat):
        start_time = time.time()
        res = list()
        print(f"Running {alg} for {model.name}")
        if alg == 'SWAY':
            res = get_sway_res(model)
        elif alg == 'RANDOM':
            res = get_random_res(model)
        elif alg == 'NSGA2':
            res = get_nsga2_res(model)
        elif alg == 'WORTHY':
            res = get_worthy_res(model)
        finish_time = time.time()
        # save the results
        with open(f'{rootpath}/results/{model.name}.{alg}.res', 'a+') as f:
            f.write('##\n')
            for i in res:
                f.write(' '.join(map(str, i.fitness.values)))
                f.write('\n')
            f.write(f'# {alg} {model.name} {finish_time-start_time}\n')