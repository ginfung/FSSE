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
from Algorithms.sway_sampler import sway, bin_dominate, cont_dominate
from Benchmarks.XOMO import XOMO, pre_defined
from repeats import request_new_file
import time
import random
import pdb


def dist(ind1, ind2):
    d = 0
    for i, j in zip(ind1, ind2):
        d += (i - j) ** 2
    return d


def where(pop):
    print(len(pop))
    rand = random.choice(pop)
    ds = [dist(i, rand) for i in pop]
    east = pop[ds.index(max(ds))]
    ds = [dist(i, east) for i in pop]
    west = pop[ds.index(max(ds))]

    c = dist(east, west)
    cc = 2 * c ** 0.5

    mappings = list()
    for x in pop:
        a = dist(x, west)
        b = dist(x, east)
        d = (a + c - b) / cc
        mappings.append((x, d))

    mappings = sorted(mappings, key=lambda i: i[1])
    mappings = [i[0] for i in mappings]

    n = len(mappings)
    eastItems = mappings[:int(n * 0.2)] + mappings[int(n * 0.5):int(n * 0.8)]
    westItems = mappings[int(n * 0.2):int(n * 0.5)] + mappings[int(n * 0.8):]

    # westItems = mappings[len(mappings)//2:]
    return west, east, eastItems, westItems


# M = None
#
# from deap.tools.emo import sortNondominated
# import numpy as np
#
#
# def where(pop):
#     while True:
#         sel = random.sample(pop, 8)
#         for i in sel:
#             M.eval(i, False)
#         front = sortNondominated(sel, 8, True)[0]
#         x = len(front)
#         non_front = [i for i in sel if i not in front]
#         if len(non_front) > 0:
#             break
#
#     east_items = list()
#     west_items = list()
#     for i in pop:
#         ds = [dist(i, j) for j in front+non_front]
#         if np.argmin(ds) < x:
#             west_items.append(i)
#         else:
#             east_items.append(i)
#     print(len(west_items), len(east_items))
#     return front[0], non_front[0], west_items, east_items


def comparing(part1, part2):
    return bin_dominate(part1, part2)


def get_sway_res(model):
    # generating the 10k random solutions
    candidates = list()
    for _ in range(10000):
        ran_dec = [random.random() for _ in range(model.decsNum)]
        can = model.Individual(ran_dec)
        candidates.append(can)
    global M
    M = model
    res = sway(candidates, model.eval, where, comparing)

    return res


if __name__ == '__main__':
    for repeat in range(1):
        ii = [0, 1, 2, 3]
        for i in ii:
            XOMO_model = pre_defined()[i]
            start_time = time.time()
            res = get_sway_res(XOMO_model)
            finish_time = time.time()
            print(finish_time - start_time)
            # save the results
            with open(request_new_file('./tse_rs/sway', XOMO_model.name), 'w') as f:
                f.write('T:' + str(start_time) + '\n~~~\n')
                f.write('T:' + str(finish_time) + '\n')
                for i in res:
                    f.write(' '.join(map(str, i.fitness.values)))
                    f.write('\n')

        print('******   ' + str(repeat) + '   ******')
