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
from deap.tools.emo import sortNondominated
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
import time
import sys
import os
import random
import random
import pdb


def random_pop(model, N):
    pop = list()
    for _ in range(N):
        pop.append(
            model.Individual([random.random() for _ in range(model.decsNum)]))
    return pop


def action(model):
    startat = time.time()
    size = 300
    init_pop = random_pop(model, size)
    for p in init_pop:
        model.eval(p, normalized=False)

    D = pd.DataFrame(data=init_pop, columns=model.decs)
    O = pd.DataFrame(data=list(map(lambda i: i.fitness.values, init_pop)))
    """
    Testing the hypothesis of FLASH
    figure(figsize=(7, 10))

    for oi, obj in enumerate(O.columns):
        plt.subplot(O.shape[1], 1, oi + 1)
        trainsize = int(size * 0.7)
        regr = DecisionTreeRegressor().fit(D.iloc[:trainsize, :],
                                           O.iloc[:trainsize, oi])
        o_pred = regr.predict(D.iloc[trainsize:, ])
        plt.xlabel(f"Actual value for o{obj}")
        plt.ylabel(f"Predict value for o{obj}")
        plt.scatter(O.iloc[trainsize:, oi], o_pred, s=7)
        plt.plot(
            O.iloc[trainsize:, oi], O.iloc[trainsize:, oi],
            color='red')  # the y=x line
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.suptitle(
        f"Build Decision tree to predict each separate obj @{model.name}")
    plt.tight_layout()
    plt.savefig(f"{model.name}_FLASH_ver.png")
    """

    # for _ in range(5):
    #     point = random.randint(0, 100)
    #     dD = D - D.iloc[point]
    #     dO = O - O.iloc[point]
    #     dist = np.square(dD).sum(axis=1)
    #     tops_i = np.argsort(dist)[:30]
    #     dD, dO = dD.iloc[tops_i], dO.iloc[tops_i]  # fetching the neighbors

    #     dO = (dO - dO.mean()
    #           ) / dO.std()  # for better viz, do the normalization for dO

    #     _keans = KMeans(n_clusters=3, random_state=0).fit(dD).labels_
    #     plt.clf()
    #     for i, col in enumerate(dO.columns):
    #         plt.scatter(dO.loc[:, col], [i] * dO.shape[0], c=_keans, s=15)

    #     # # plt.title(model.name)
    #     # #3 plt.savefig(f"{model.name}_global.png")
    #     plt.show()

    sys.exit(0)
    return res
