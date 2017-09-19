from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pickle
from scipy.stats import ttest_ind
from numpy import median
import scipy
import pdb
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


def plot(model, t_i, yround=4, lessIsBetter=True):
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

    data = [sanity, ground, sway, moea]
    maxy = max(max(sanity), max(ground), max(sway), max(moea)) * 1.2

    if t_i == 2: data = data[1:]

    fig = plt.figure(1, figsize=(3.5, 2.3))
    ax = fig.add_subplot(111)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_ylim([0, maxy])
    ax.set_xlim([0.1, 1.8])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    y_ticks = [0, maxy * 0.25, maxy * 0.5, maxy * 0.75, maxy]
    y_ticks = [round(i, yround) for i in y_ticks]
    x_ticks = [0.5, 0.95, 1.4, 1.85]
    if t_i == 2:
        y_ticks = y_ticks[:-1]
        x_ticks = x_ticks[:-1]
    ax.set_yticks(y_ticks)

    pos1 = ax.get_position()  # get the original position
    pos2 = [pos1.x0 + 0.3, pos1.y0 + yround * 0.2, pos1.width, pos1.height]
    ax.set_position(pos2)  # set a new position

    box = ax.boxplot(data, patch_artist=True, widths=0.3, positions=x_ticks, showfliers=False)
    plt.tick_params(
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
    elif (lessIsBetter and median(ground) < median(moea)) or ((not lessIsBetter) and median(ground) > median(moea)):
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
    elif (lessIsBetter and median(sway) < median(moea)) or ((not lessIsBetter) and median(sway) > median(moea)):
        colors.append(green[0])
        fcolors.append(green[1])
    else:
        colors.append(red[0])
        fcolors.append(red[1])

    colors.append(orange[0])
    fcolors.append(orange[1])
    # pdb.set_trace()

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
        plt.title(y_titles[t_i], style='italic', fontsize=10)
    if t_i == 0:
        plt.ylabel(model, fontsize=10)

    if model == 'linux':
        plt.tick_params(labelbottom='on')
        if t_i == 2:
            plt.xticks(x_ticks, ['GROUND', 'SWAY', 'MOEA'], rotation=30)
        else:
            plt.xticks(x_ticks, ['RAND', 'GROUND', 'SWAY', 'MOEA'], rotation=30)
            # ax.set_xticklabels(['RAND', 'GROUND', 'SWAY', 'MOEA'])

    # plt.show()
    tmp_fold = ['gd', 'gs', 'pfs', 'hv']
    fig.savefig('./' + tmp_fold[t_i] + '/' + model + '.png', bbox_inches='tight')
    plt.clf()


# def combining():
#     pass


if __name__ == '__main__':
    for m in ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c', 'webportal', 'eshop', 'fiasco', 'freebsd',
              'linux']:
        print(m)
        plot(m, 0, 4, True)
        plot(m, 1, 2, True)
        plot(m, 2, 0, False)
        plot(m, 3, 2, False)
        # combining()
