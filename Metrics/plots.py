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
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pickle


class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of
    magnitude"""

    def __init__(self, order_of_mag=0, useOffset=True, useMathText=False):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(self, useOffset=useOffset,
                                 useMathText=useMathText)

    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag


def plot(model, t_i):
    """
    :param model:
    :param t_i: 0-gd, 1-gs, 2-pfs, 3-hv
    :return:
    """
    with open('../Experiments/tse_rs/all.stat', 'r') as f:
        data = pickle.load(f)
        data = data[model]

    ground = data['ground'][t_i]
    sway = data['sway'][t_i]
    moea = data['moea'][t_i]
    # sway = [i - 0.0001 for i in sway]
    # pdb.set_trace()
    print(sum(sway)/len(sway))
    print(sum(moea)/len(moea))

    data = [ground, sway, moea]
    maxy = max(max(ground), max(sway), max(moea)) * 1.2
    miny = min(min(ground), min(sway), min(moea)) * 0.8

    fig = plt.figure(1, figsize=(4.5, 2.3))
    ax = fig.add_subplot(111)
    # ax.set_xticklabels(['GROUND', 'SWAY', 'MOEA'])
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_ylim([miny, maxy])
    ax.set_xlim([0.1, 1.8])

    box = ax.boxplot(data, patch_artist=True, widths=0.3, positions=[0.5, 1, 1.5], showfliers=False)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='major',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        right='off',
        labelbottom='off')  # labels along the bottom edge are off

    # colors = ['green', 'orange', 'red']
    # for b, col in zip(box['boxes'], colors):
    #     b.set(color=col, facecolor='white')
    #     b.set_facecolor(col)

    # ax.yaxis.set_major_formatter(FixedOrderFormatter(-2))
    ax.get_yaxis().get_major_formatter().set_useOffset(True)
    # plt.show()
    fig.savefig('./gd/' + model + '.png', bbox_inches='tight')
    plt.clf()


if __name__ == '__main__':
    for m in ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c', 'webportal', 'eshop', 'fiasco', 'freebsd',
              'linux']:
        # for m in ['osp']:
        print(m)
        plot(m, 0)
