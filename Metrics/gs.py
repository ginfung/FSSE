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
import operator


def dist(a, b):
    return sum((i-j)**2 for i, j in zip(a, b))


def GS(PF0, PFc):
    # get all e_k
    e_k = list()
    for col in zip(*PF0):
        min_index, min_value = min(enumerate(col), key=operator.itemgetter(1))
        e_k.append(PF0[min_index])

    dl = 0
    for c in e_k:
        dl += min([dist(c, i) for i in PFc])

    d2 = list()
    for s in PFc:
        d = 'inf'
        for o in PFc:
            if s == o: continue
            d = min(d, dist(s, o))
        d2.append(d)
    meand = sum(d2) / len(d2)
    dr = sum([abs(i - meand) for i in d2])
    gs = (dl + dr) / (dl + len(d2) * meand)

    return gs