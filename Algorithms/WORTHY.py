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
    # startat = time.time()
    # init_pop = random_pop(model, 100)
    # for p in init_pop:
    #     model.eval(p, normalized=False)
    """
    # Testing the hypothesis of FLASH
    size = 100
    figure(figsize=(7, 10))

    D = pd.DataFrame(data=init_pop, columns=model.decs)
    O = pd.DataFrame(data=list(map(lambda i: i.fitness.values, init_pop)))
    for oi, obj in enumerate(O.columns):
        plt.subplot(O.shape[1], 1, oi + 1)
        trainsize = int(size * 0.7)
        regr = DecisionTreeRegressor().fit(D.iloc[:trainsize, :],
                                           O.iloc[:trainsize, oi])
        o_pred = regr.predict(D.iloc[trainsize:, ])
        o_pred = pd.DataFrame(
            o_pred, index=range(trainsize, size), columns=[oi])
        o_actual = pd.DataFrame(O.iloc[trainsize:, :], columns=O.columns)

        actual_idx = np.array(o_actual.sort_values(by=obj).index)
        pred_idx = np.array(o_pred.sort_values(by=obj).index)

        idx_delta = (pred_idx - actual_idx) / (o_pred.shape[0])
        idx_delta = sorted(idx_delta)
        plt.scatter(range(o_pred.shape[0]), idx_delta, s=7)
        plt.ylabel("(Rank delta)/totalCase")
        # plt.xlabel(f"Actual idx for o{obj}")
        # plt.ylabel(f"Predict value for o{obj}")
        # plt.scatter(o_actual[obj], o_pred[obj], s=7)
        # plt.plot(o_actual[obj], o_actual[obj], color='red')  # the y=x line
        # plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.suptitle(
        f"Build Decision tree to predict each separate obj @{model.name}")
    plt.tight_layout()
    plt.savefig(f"{model.name}_FLASH_ver_deltaRank.png")
    # plt.show()
    """
    """
    Build learner for each objective dO = f(dD) ??
    
    figure(figsize=(7, 10))
    dD, dO = list(), list()
    for i in range(size):
        for j in range(i, size):
            dD.append(D.iloc[i] - D.iloc[j])
            dO.append(O.iloc[i] - O.iloc[j])
    dD = pd.DataFrame(dD, index=range(len(dD)))
    dO = pd.DataFrame(dO, index=range(len(dO)))

    assert not (dO.std() < 0).any()
    dO = (dO - 0) / dO.std()  # do the normalize with 0 as mean
    for oi, obj in enumerate(dO.columns):
        X_train, X_test, y_train, y_test = train_test_split(
            dD, dO[obj], test_size=0.33)
        regr = KNeighborsRegressor(n_neighbors=4).fit(X_train, y_train)
        y_pred = regr.predict(X_test)

        plt.subplot(dO.shape[1], 1, oi + 1)
        plt.scatter(y_test, y_pred, s=3)

        plt.plot([0] * len(y_pred), y_pred, color='red')
        plt.plot(y_test, [0] * len(y_test), color='red')
        plt.plot(y_test, y_test, color='red')

    plt.tight_layout()
    plt.savefig(f"{model.name}_map_delta.png")
    # ax = plt.axes(projection='3d')
    # for idx in front_idx[0]:
    #     ax.scatter3D(O.iloc[idx, 0], O.iloc[idx, 1], O.iloc[idx, 2], c='red')
    #     ax.text(O.iloc[idx, 0], O.iloc[idx, 1], O.iloc[idx, 2], '0')
    """
    """
    while True:
        print(f"size of pop = {len(pop)}")
        D = pd.DataFrame(data=pop, columns=model.decs)
        O = pd.DataFrame(data=list(map(lambda i: i.fitness.values, pop)))
        dD, dO = list(), list()
        for i in range(len(pop)):
            for j in range(i, len(pop)):
                dD.append(D.iloc[i] - D.iloc[j])
                dO.append(O.iloc[i] - O.iloc[j])
        dD = pd.DataFrame(dD, index=range(len(dD)))
        dO = pd.DataFrame(dO, index=range(len(dO)))

        assert not (dO.std() < 0).any()
        dO = (dO - 0) / dO.std()  # do the normalize with 0 as mean
        regr = list()
        for oi, obj in enumerate(dO.columns):
            regr_tmp = KNeighborsRegressor(n_neighbors=4).fit(dD, dO[obj])
            regr.append(regr_tmp)

        front_idx = _emo_sortNondominated_idx(pop, first_front_only=True)[0]
        next_pop = [pop[i] for i in front_idx]

        for p in next_pop:
            print(p.fitness.values)
        print('----')

        # new_candidates = list()
        for each_front_idx in front_idx:
            # random gen bunches of neighbors
            mut_dD = list()
            for _ in range(100):
                mut_dD.append(D.loc[each_front_idx] * np.random.normal(
                    0, 0.5, D.shape[1]))
            mut_dD = pd.DataFrame(mut_dD, index=range(len(mut_dD)))
            mut_dO = pd.DataFrame(columns=dO.columns)
            # predicting mut_dO
            for oi, obj in enumerate(mut_dO.columns):
                mut_dO[obj] = regr[oi].predict(mut_dD)

            # select some and eval
            # for i in mut_dD.index:
            #     tmp_can = model.Individual(D.loc[each_front_idx] +
            #                                mut_dD.loc[i])
            #     tmp_can.fitness.values = O.loc[each_front_idx] + mut_dO.loc[i]
            #     new_candidates.append(tmp_can)
            filtered = (mut_dO < -0.5).any(axis=1)
            new_decs = D.loc[each_front_idx] + mut_dD[filtered]
            for nd in new_decs.index:
                candidate = model.Individual(new_decs.loc[nd])
                model.eval(candidate, normalized=False)
                next_pop.append(candidate)

        # for nd in _emo_sortNondominated_idx(
        #         new_candidates, first_front_only=True)[0]:
        #     next_pop.append(new_candidates[nd])
        #     model.eval(next_pop[-1], normalized=False)
        pop = next_pop
    """

    startat = time.time()
    next_pops_pool = list()
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
            est_pf_idx = _emo_sortNondominated_idx(
                next_pop, first_front_only=True)[0]

            guess_pf = [pop[fi]]

            for epi in est_pf_idx:
                model.eval(next_pop[epi], normalized=False)
                guess_pf.append(next_pop[epi])

            really_pf = emo.sortNondominated(guess_pf, len(guess_pf), True)[0]
            next_pops_pool.extend(really_pf)

            # print(
            #     f"Success guess rate: {len(really_pf_idx)/len(est_pf_idx)*100}%, Find anyway? {len(really_pf_idx)>=1}"
            # )
    return emo.sortNondominated(
        next_pops_pool, len(next_pops_pool), first_front_only=True)[0]
