from __future__ import division
from deap import creator, base
from deap.tools.emo import sortNondominated
from Metrics.hv import HyperVolume
from Metrics.gd import GD
from Metrics.gs import GS
from repeats import fetch_all_files
import numpy
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


def median(lst):
    return numpy.median(numpy.array(lst))


def _get_frontier(pop):
    """
    return the pareto frontier of the given pop. No duplicate individuals in the returns
    :param pop:
    :return:
    """
    front = sortNondominated(pop, len(pop), True)[0]
    uniques = []
    for f in front:
        if f not in uniques:
            uniques.append(f)
    return uniques


def put_record_here(filename, model):
    def calc(PFc):
        creator.create("FitnessMin", base.Fitness, weights=[-1.0] * len(PFc[0]))
        creator.create("Individual", str, fitness=creator.FitnessMin)

        pop = list()
        for sol in PFc:
            ind = creator.Individual(str(sol))  # a trick here... use the fitness to identify solutions
            ind.fitness = creator.FitnessMin(sol)
            pop.append(ind)

        del PFc
        PFc = pop[:]
        del pop
        PFc = _get_frontier(PFc)  # DEAP version
        PFc_list = [i.fitness.values for i in PFc]  # PYTHON LIST version
        if len(PFc) < MINIMUM_PFS:
            return model, -1, -1, len(PFc), -1, PFc

        # GD
        # load the PF0
        PF0 = list()
        with open('./PF_0/' + model + '.txt', 'r') as f:
            for l in f:
                e = l.strip('\n').split(' ')
                e = [float(i) for i in e]
                PF0.append(e)
        gd = GD(PF0, PFc_list)

        # GS
        gs = GS(PF0, PFc_list)
        # PFS
        pfs = len(PFc)
        # HV
        rp = [1] * len(PFc[0].fitness.values)  # reference point

        hv = HyperVolume(rp).compute(PFc_list)
        hv = round(hv, 4)

        return model, gd, gs, pfs, hv, PFc

    with open(filename, 'r') as f:
        content = f.readlines()
    content = map(lambda l: l.strip('\n'), content)
    if content[-1].startswith('~~~'):
        content = content[:-1]

    times = list()
    PFc = []

    for l in content:
        if l.startswith('T:'):
            times.append(float(l[2:]))
            continue
        if l.startswith('Gen:'):
            continue
        if l.startswith('~~~'):
            PFc = []
            continue
        # filtering for SPL
        e = l.split(' ')
        e = [round(float(i), 3) for i in e]
        if PRODUCT_LINE_ONLY:
            if e[0] > 0.00001:
                continue
            e = e[1:]
        PFc.append(e)

    if len(PFc) == 0:
        pdb.set_trace()

    model, gd, gs, pfs, hv, _ = calc(PFc)
    return model, gd, gs, pfs, hv


SOURCE_FOLDER = "/Users/jianfeng/Desktop/tse_rs/"

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    models = ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c']
    models += ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']

    spls = ['webportal', 'eshop', 'fiasco', 'freebsd', 'linux']

    all_stat = dict()
    for name in models:
        if name in spls:
            PRODUCT_LINE_ONLY = True
        else:
            PRODUCT_LINE_ONLY = False

        all_stat[name] = dict()
        files = fetch_all_files(SOURCE_FOLDER + 'god', name)
        gd, gs, pfs, hv = list(), list(), list(), list()
        for f in files:
            _, a, b, c, d = put_record_here(f, name)
            if c < MINIMUM_PFS:
                continue
            gd.append(a)
            gs.append(b)
            pfs.append(c)
            hv.append(d)
        all_stat[name]['ground'] = (gd, gs, pfs, hv)

        ###############
        files = fetch_all_files(SOURCE_FOLDER + 'sway', name)
        gd, gs, pfs, hv = list(), list(), list(), list()
        for f in files:
            _, a, b, c, d = put_record_here(f, name)

            if c < MINIMUM_PFS:
                continue
            gd.append(a)
            gs.append(b)
            pfs.append(c)
            hv.append(d)

        all_stat[name]['sway'] = (gd, gs, pfs, hv)

        ###############
        if PRODUCT_LINE_ONLY:
            files = fetch_all_files(SOURCE_FOLDER + 'satibea', name)
        else:
            files = fetch_all_files(SOURCE_FOLDER + 'nsga2', name)

        gd, gs, pfs, hv = list(), list(), list(), list()
        for f in files:
            _, a, b, c, d = put_record_here(f, name)
            if c < MINIMUM_PFS:
                continue
            gd.append(a)
            gs.append(b)
            pfs.append(c)
            hv.append(d)

        all_stat[name]['moea'] = (gd, gs, pfs, hv)

        ###############
        files = fetch_all_files(SOURCE_FOLDER + 'sanity', name)
        gd, gs, pfs, hv = list(), list(), list(), list()
        for f in files:
            _, a, b, c, d = put_record_here(f, name)

            if c < MINIMUM_PFS:
                continue
            gd.append(a)
            gs.append(b)
            pfs.append(c)
            hv.append(d)

        all_stat[name]['sanity'] = (gd, gs, pfs, hv)

        print(name)

    pickle.dump(all_stat, open('../Experiments/tse_rs/all.stat', 'wb'))
    print(all_stat)

