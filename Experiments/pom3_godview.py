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
from Benchmarks.POM3 import pre_defined
from repeats import request_new_file
import time
import random
import pdb
import debug


def action(model):
    start_time = time.time()
    # generating the 10k random solutions
    candidates = list()
    for _ in range(10000):
        ran_dec = [random.random() for _ in range(model.decsNum)]
        can = model.Individual(ran_dec)
        candidates.append(can)
    print('random sol created.')
    for can in candidates:
        model.eval(can)
    print('finish evaluating.')
    res = emo.sortNondominated(candidates, len(candidates), True)
    print('finish selection.')
    finish_time = time.time()
    with open(request_new_file('./tse_rs/god', model.name), 'w') as f:
        f.write('T:' + str(start_time) + '\n~~~\n')
        f.write('T:' + str(finish_time) + '\n')
        for front in res[0]:
            f.write(' '.join(map(str, front.fitness.values)))
            f.write('\n')

        f.write('~~~\n')

    return res


if __name__ == '__main__':
    for repeat in range(1):
        ii = [0, 1, 2]
        for i in ii:
            print(i)
            POM3_model = pre_defined()[i]
            res = action(POM3_model)

        print('******   ' + str(repeat) + '   ******')
