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

from deap import algorithms
from deap import tools
from deap.tools import emo
from deap.tools.emo import sortNondominated
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.model_selection import train_test_split
from mpl_toolkits import mplot3d
from matplotlib.pyplot import figure
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import sys
import os
import random
import random
import pdb


def _emo_sortNondominated_idx(pop, first_front_only=False):
    fronts = emo.sortNondominated(
        pop, len(pop), first_front_only=first_front_only)
    return [[pop.index(i) for i in f] for f in fronts]


def random_pop(model, N):
    pop = list()
    for _ in range(N):
        pop.append(
            model.Individual([random.random() for _ in range(model.decsNum)]))
    return pop


def action_expr(model):
    startat = time.time()
    samples = random_pop(model, 100)
    for p in samples:
        model.eval(p, normalized=False)
    print("100 init pop evaluated.")

    for round_ in range(10):
        samples.extend(random_pop(model, 20))
        for p in samples[-20:]:
            model.eval(p, normalized=False)
        D = pd.DataFrame(data=samples, columns=model.decs)
        O = pd.DataFrame(data=list(map(lambda i: i.fitness.values, samples)))
        front_idx = _emo_sortNondominated_idx(
            samples, first_front_only=True)[0]

        next_pop = list()
        for fi in front_idx:
            dist_order = (D - D.loc[fi]).abs().pow(2).sum(
                axis=1).sort_values().index[1:int(len(samples) * 0.1) +
                                            1]  # fetch the top 10% of samples
            dD, dO = list(), list()
            for i in dist_order:
                for j in dist_order:
                    if i == j: continue
                    dD.append(D.iloc[i] - D.iloc[j])
                    dO.append(O.iloc[i] - O.iloc[j])
            dD = pd.DataFrame(dD, index=range(len(dD)))
            dO = pd.DataFrame(dO, index=range(len(dO)))
            assert not (dO.std() < 0).any()

            regr = list()
            for oi, obj in enumerate(dO.columns):
                regr_tmp = KNeighborsRegressor(n_neighbors=4).fit(dD, dO[obj])
                regr.append(regr_tmp)

            mut_dD = list()
            for _ in range(D.shape[1] * 2):
                mut_dD.append(D.loc[fi] * np.random.normal(0, 0.5, D.shape[1]))
            mut_dD = pd.DataFrame(mut_dD, index=range(len(mut_dD)))
            mut_dO = pd.DataFrame(columns=dO.columns)
            for oi, obj in enumerate(mut_dO.columns):
                mut_dO[obj] = regr[oi].predict(mut_dD)
            filtered = (mut_dO < -1 * mut_dO.std()).any(axis=1)
            new_decs = D.loc[fi] + mut_dD[filtered]
            print('new eval = ', str(new_decs.shape[0]))
            for nd in new_decs.index:
                candidate = model.Individual(new_decs.loc[nd])
                model.eval(candidate, normalized=False)
                next_pop.append(candidate)

        samples.extend(emo.sortNondominated(next_pop, len(next_pop), True)[0])
        print(f'Round {round_} done. Sample size = {len(samples)}')
    return emo.sortNondominated(
        samples, len(samples), first_front_only=True)[0]


def action_expr2(model):
    startat = time.time()
    for round_ in range(10):
        init_pop = random_pop(model, 100)
        for p in init_pop:
            model.eval(p, normalized=False)
        pop = init_pop
        print("100 init pop evaluated.")
        # first round
        D = pd.DataFrame(data=pop, columns=model.decs)
        O = pd.DataFrame(data=list(map(lambda i: i.fitness.values, pop)))
        front_idx = _emo_sortNondominated_idx(pop, first_front_only=True)[0]

        guess_pf = list()
        for fi in front_idx:
            dist_order = (D - D.loc[fi]).abs().pow(2).sum(
                axis=1).sort_values().index[1:int(len(pop) * 0.1) +
                                            1]  # fetch the top 10% of pop
            dD, dO = list(), list()
            for i in dist_order:
                for j in dist_order:
                    if i == j: continue
                    dD.append(D.iloc[i] - D.iloc[j])
                    dO.append(O.iloc[i] - O.iloc[j])
            dD = pd.DataFrame(dD, index=range(len(dD)))
            dO = pd.DataFrame(dO, index=range(len(dO)))
            assert not (dO.std() < 0).any()

            regr = list()
            for oi, obj in enumerate(dO.columns):
                regr_tmp = KNeighborsRegressor(n_neighbors=4).fit(dD, dO[obj])
                regr.append(regr_tmp)

            mut_dD, next_pop = list(), list()
            for _ in range(D.shape[1] * 2):
                mut_dD.append(D.loc[fi] * np.random.normal(0, 0.5, D.shape[1]))
            mut_dD = pd.DataFrame(mut_dD, index=range(len(mut_dD)))
            mut_dO = pd.DataFrame(columns=dO.columns)
            for oi, obj in enumerate(mut_dO.columns):
                mut_dO[obj] = regr[oi].predict(mut_dD)
            filtered = (mut_dO < -0.5 * mut_dO.std()).any(axis=1)
            new_decs = D.loc[fi] + mut_dD[filtered]

            for nd in new_decs.index:
                candidate = model.Individual(new_decs.loc[nd])
                candidate.fitness.values = O.loc[fi] + mut_dO.loc[nd]
                next_pop.append(candidate)

            guess_pf.append(pop[fi])
            guess_pf.extend(next_pop)

        guess_pf = emo.sortNondominated(guess_pf, len(guess_pf), True)[0]
        for i in range(len(guess_pf)):
            model.eval(guess_pf[i], normalized=False)
        next_pops_pool.extend(guess_pf)

        # print(
        #     f"Success guess rate: {len(really_pf_idx)/len(est_pf_idx)*100}%, Find anyway? {len(really_pf_idx)>=1}"
        # )
    return emo.sortNondominated(
        next_pops_pool, len(next_pops_pool), first_front_only=True)[0]