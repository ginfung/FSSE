from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pickle
from scipy.stats import ttest_ind
from numpy import median
import scipy
import numpy
import debug


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


y_titles = ['Generational Distance', 'Genearted Spread', 'Pareto Front Size', 'Hypervolume']


def bound(x):
    q25, q75 = numpy.percentile(x, [25, 75])
    iqr = q75 - q25
    m = median(x)
    return m - 1.5 * iqr, m + 1.5 * iqr


def plot(model, t_i, yround=4, lessIsBetter=True, ax=None):
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
    sanity = data['sanity'][t_i]

    if t_i == 2:
        sanity = sway  # useless

    data = [sanity, ground, sway, moea]

    if t_i == 2: data = data[1:]

    # fig = plt.figure(1, figsize=(3.5, 2.3))
    # ax = plt.subplot(12, 4, panelId)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xlim([0.1, 1.8])
    x_ticks = [0.5, 0.95, 1.4, 1.85]

    if t_i == 2:
        x_ticks = x_ticks[:-1]

    box = ax.boxplot(data, patch_artist=True, widths=0.3, positions=x_ticks, showfliers=False)

    miny = min(bound(ground)[0], bound(sway)[0], bound(moea)[0], bound(sanity)[0])
    if miny < 0: miny = 0
    maxy = max(bound(ground)[1], bound(sway)[1], bound(moea)[1], bound(sanity)[1])
    miny *= 0.8
    maxy *= 1.2

    ax.set_ylim([miny, maxy])
    miny = round(miny, yround)
    maxy = round(maxy, yround)
    y_ticks = [miny,
               # miny + (maxy - miny) * 0.44,
               miny + (maxy - miny) * 0.45, maxy * 0.90]
    y_ticks = [round(i, yround) for i in y_ticks]

    ax.set_yticks(y_ticks)
    ax.tick_params(labelsize=6)

    ax.tick_params(
        axis='x',  # changes apply to the x-axis
        which='major',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        right='off',
        labelbottom='off')  # labels along the bottom edge are off

    red = ['red', '#FFE6E6']
    green = ['green', '#76E959']
    orange = ['orange', '#FFE5CC']

    colors = ['black']
    fcolors = ['#B2B2B2']

    les = min(len(ground), len(moea))
    p = scipy.stats.wilcoxon(ground[:les], moea[:les])[1]
    if p < 0.005 and (abs(median(ground) - median(moea)) < median(moea) * 0.1):
        colors.append(orange[0])
        fcolors.append(orange[1])
    elif (lessIsBetter and median(ground) - median(moea) < median(moea) * 0.1) or (
                (not lessIsBetter) and median(ground) - median(moea) > -median(moea) * 0.1):
        colors.append(green[0])
        fcolors.append(green[1])
    else:
        colors.append(red[0])
        fcolors.append(red[1])

    les = min(len(sway), len(moea))
    p = scipy.stats.wilcoxon(sway[:les], moea[:les])[1]

    # pdb.set_trace()
    if p < 0.005 and (abs(median(sway) - median(moea)) < median(moea) * 0.1):
        colors.append(orange[0])
        fcolors.append(orange[1])
    elif (lessIsBetter and median(sway) - median(moea) < median(moea) * 0.1) or (
                (not lessIsBetter) and median(sway) - median(moea) > -median(moea) * 0.1):
        colors.append(green[0])
        fcolors.append(green[1])
    else:
        colors.append(red[0])
        fcolors.append(red[1])

    colors.append(orange[0])
    fcolors.append(orange[1])

    if t_i == 2:
        colors = colors[1:]
        fcolors = fcolors[1:]

    for ml, b, col, fcol in zip(box['medians'], box['boxes'], colors, fcolors):
        b.set_color(col)
        b.set(facecolor=fcol)
        ml.set_color(col)  # median

    # ax.yaxis.set_major_formatter(FixedOrderFormatter(-2))
    ax.get_yaxis().get_major_formatter().set_useOffset(True)

    if model == 'osp':
        ax.set_title(y_titles[t_i], style='italic', fontsize=6)
    if t_i == 0:
        ax.set_ylabel(model, fontsize=6)

    if model == 'linux':
        ax.tick_params(labelbottom='on')
        if t_i == 2:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(('GT', 'SWAY', 'MOEA'), fontsize=6, rotation=50)
        else:
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(['RAND', 'GT', 'SWAY', 'MOEA'], fontsize=6, rotation=50)


if __name__ == '__main__':
    tPlot, axes = plt.subplots(nrows=12, ncols=4, figsize=(6, 7))
    for i, m in enumerate(
            ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c', 'webportal', 'eshop', 'fiasco', 'freebsd',
             'linux']):
        print(m)
        plot(m, 0, 4, True, axes[i][0])
        plot(m, 1, 2, True, axes[i][1])
        plot(m, 2, 0, False, axes[i][2])
        plot(m, 3, 2, False, axes[i][3])

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.show()

    # using python tool. save as XXX.pdf
