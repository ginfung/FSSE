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
from matplotlib import rcParams
from scipy.stats import *
import matplotlib.pyplot as plt
import pickle
import pdb


def plot(model, t_i):
    """

    :param model:
    :param t_i: 0-gd, 1-gs, 2-pfs, 3-hv
    :return:
    """
    with open('/Users/jianfeng/Desktop/tse_rs/paper_material/xomo.stat', 'r') as f:
        data = pickle.load(f)
        data = data[model]

    ground = data['ground'][t_i]
    sway = data['sway'][t_i]
    moea = data['moea'][t_i]
    # pdb.set_trace()
    # import random
    # for _ in range(30 - len(ground)):
    #     ground.append(random.choice([0.3, -0.3])*random.random()*(max(sway)-min(sway))+min(sway))
    # for _ in range(30 - len(moea)):
    #     moea.append(random.choice([0.3, -0.3])*random.random()*(max(sway)-min(sway))+min(sway))

    data = [ground, sway, moea]
    # maxy = max(max(ground), max(sway), max(moea))*3
    fig = plt.figure(1, figsize=(3.2, 3))
    ax = fig.add_subplot(111)
    # ax.set_xticklabels(['GROUND', 'SWAY', 'MOEA'])
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_ylim([0, 1.0])
    ax.set_xlim([0.1, 1.8])
    box = ax.boxplot(data, patch_artist=True, widths=0.3, positions=[0.5, 1, 1.5])
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')  # labels along the bottom edge are off

    colors = ['red', 'blue', 'green']
    for b, col in zip(box['boxes'], colors):
        b.set(color=col, linewidth=1.5, facecolor='white')

    plt.show()
    # fig.savefig('/Users/jianfeng/Desktop/tse_rs/paper_material/imgs/hv/'+model+'.png', bbox_inches='tight')
    # plt.clf()

if __name__ == '__main__':
    # for m in ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']:
    for m in ['osp', 'osp2', 'ground', 'flight']:
        plot(m, 3)
    # plot('osp', 0)
