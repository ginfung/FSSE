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
import time
import pdb
import debug

"""
Evaluating all 10k SAT solver results, then use usga-ii sorting to get the frontier
"""


def action(fm):
    # laod the 10k sat solutions
    candidates = list()
    with open('/Users/jianfeng/Desktop/tse_rs/' + fm.name + '.txt', 'r') as f:
        for l in f:
            can = fm.Individual(l.strip('\n'))
            candidates.append(can)
    # evaluate all
    start_time = time.time()
    for can in candidates:
        fm.eval(can)
    #     o = (round(i, 2) for i in can.fitness.values)
    #     can.fitness.values = o
    #
    # candidates.sort(key=lambda i: i.fitness.values)
    # x = 0
    # for k, g in groupby(candidates, key=lambda i: i.fitness.values):
    #     x += 1
    #     print(k)
    # pdb.set_trace()
    mid_time = time.time()

    res = emo.sortNondominated(candidates, len(candidates), True)
    finish_time = time.time()

    with open(request_new_file('/Users/jianfeng/Desktop/tse_rs/god', fm.name), 'w') as f:
        f.write('T:'+str(start_time)+'\n~~~\n')
        f.write('T:'+str(finish_time)+'\n')
        for front in res[0]:
            f.write(' '.join(map(str, front.fitness.values)))
            f.write('\n')

        f.write('~~~\n')

if __name__ == '__main__':
    for repeat in range(6):
        models = ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']
        # models = ['webportal']
        for name in models:
            model = DimacsModel(name)
            action(model)
            print(name)
