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
import random
import pdb

p = DimacsModel('webportal')
# 'webportal', 'eshop',  'fiasco', 'freebsd', 'linux'

with open('/Users/jianfeng/Desktop/tse_rs/webportal.txt', 'r') as f:
    candidates = list()
    for l in f:
        candidates.append(l[:-1])
    candidates = random.sample(candidates, 100)

can = list()
for i in candidates:
    can.append(p.Individual(i))
del candidates

for i in can:
    p.eval(i)
    # print(i.fitness.values)

with open('/Users/jianfeng/Desktop/tse_rs/random/webportal.txt', 'w') as f:
    for i in can:
        f.write(str(i.fitness.values)[1:-1])
        f.write('\n')

# pdb.set_trace()