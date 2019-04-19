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

from deap import creator, base
from deap.tools.emo import sortNondominated
import pygmo
from Metrics.gd import GD
from Metrics.gs import GS
from repeats import fetch_all_files
import numpy as np
import pandas as pd
import warnings
import pickle
import pdb

PRODUCT_LINE_ONLY = False
MINIMUM_PFS = 3
"""
GD
GS
GFS
HV
"""


def identify_pareto(scores):
    mask = [True] * scores.shape[0]
    for i in range(scores.shape[0]):
        if (scores.iloc[:i] <= scores.iloc[i]).all(axis=1).any():
            mask[i] = False
        elif (scores.iloc[i + 1:] <= scores.iloc[i]).all(axis=1).any():
            mask[i] = False
    return mask


def global_info(model):
    all_res = list()
    for file in os.listdir("../results"):
        if f"{model}." in file and '.res' in file:
            with open(f"../results/{file}") as f:
                for line in f.readlines():
                    if line.startswith('#'): continue
                    all_res.append(line[:-1].split(' '))
    objs_df = pd.DataFrame(all_res).convert_objects(convert_numeric=True)
    front_idx = identify_pareto(objs_df)

    objs_df.describe().to_pickle(f'PF_0/{model}_summary.pkl')
    objs_df[front_idx].reset_index(drop=True).to_pickle(f'PF_0/{model}_pf.pkl')


def get_metrics(expr, fronts, front_srz):
    # step 1 do the normalization
    maxs, mins = front_srz.loc['max'], front_srz.loc['min']
    expr_normed = (expr - mins) / (maxs - mins)
    fronts_normed = (fronts - mins) / (maxs - mins)

    # step2 calc the hypervolume
    hv = pygmo.hypervolume(expr_normed.values.tolist()).compute(
        [1] * expr.shape[1])

    # step3 get the gd (general distance)
    gd = GD(fronts_normed.values, expr_normed.values)

    # step4 get the gs (general spread)
    gs = GS(fronts_normed.values, expr_normed.values)

    # step5 get the PFS in case someone need that
    pfs = expr_normed.shape[0]

    return hv, gd, gs, pfs


def MAIN(model, alg):
    fronts = pd.read_pickle(f'PF_0/{model}_pf.pkl')
    front_srz = pd.read_pickle(f'PF_0/{model}_summary.pkl')
    stats = list()
    with open(f"../results/{model}.{alg}.res", 'r') as f:
        res = list()
        for line in f.read().splitlines():
            if line.startswith('##'):
                res.clear()
                continue
            if line.startswith('# '):
                expr = pd.DataFrame(res).convert_objects(convert_numeric=True)
                hv, gd, gs, pfs = get_metrics(expr, fronts, front_srz)
                stats.append([hv, gd, gs, pfs])
                print('.', end='')
            res.append(line.split(' '))

    stats_df = pd.DataFrame(stats, columns=['hv', 'gd', 'gs', 'pfs'])
    stats_df.to_pickle(f'../results/{model}.{alg}.stats.pkl')
    print('!DONE!')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    models = ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c']

    # for model in models:
    #     global_info(model)
    #     print(f"{model} global_info Done.")

    for model in models:
        for alg in ['NSGA2', 'RANDOM', 'SWAY']:
            print(f'Calculating {model} @ {alg}.')
            MAIN(model, alg)