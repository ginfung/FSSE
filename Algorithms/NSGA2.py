from __future__ import division

from deap import algorithms
from deap import tools
from deap.tools.emo import sortNondominated
from Metrics.gs import GS
from Metrics.gd import GD
from Metrics.hv import HyperVolume
import copy
import time
import numpy
import os
import random
import debug
import pdb


def random_pop(model, N):
    pop = list()
    for _ in range(N):
        pop.append(model.Individual([random.random() for _ in range(model.decsNum)]))
    return pop


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


def self_stats(pop, model, PF0):
    PFc = _get_frontier(pop)
    PFc_list = [i.fitness.values for i in PFc]
    gd = GD(PF0, PFc_list)
    gs = GS(PF0, PFc_list)
    pfs = len(PFc)
    rp = [1] * len(PFc[0].fitness.values)  # reference point

    hv = HyperVolume(rp).compute(PFc_list)
    hv = round(hv, 4)
    return (gd, gs, pfs, hv)


def action(model, mu, ngen, cxpb, mutpb):
    toolbox = model.toolbox

    toolbox.register('mate', tools.cxOnePoint)
    toolbox.register('mutate', tools.mutPolynomialBounded, low=0, up=1.0, eta=20.0, indpb=1.0 / model.decsNum)
    toolbox.register('select', tools.selNSGA2)

    stats = tools.Statistics(lambda ind: ind)
    PF0 = list()
    with open(os.path.dirname(os.path.abspath(__file__))+'/../Metrics/PF_0/' + model.name + '.txt', 'r') as f:
        for l in f:
            e = l.strip('\n').split(' ')
            e = [float(i) for i in e]
            PF0.append(e)
    stats.register("gd_gs_pfs_hv", self_stats, model=model, PF0=PF0)

    logbook = tools.Logbook()
    logbook.header = "gen", "gd_gs_pfs_hv"

    pop = random_pop(model, mu)
    for p in pop:
        model.eval(p)

    pop = toolbox.select(pop, len(pop))
    t = time.time()
    for gen in range(1, ngen):
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [copy.deepcopy(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= cxpb:
                toolbox.mate(ind1, ind2)

            if random.random() <= mutpb:
                toolbox.mutate(ind1)
                toolbox.mutate(ind2)

            model.eval(ind1)
            model.eval(ind2)

        pop = toolbox.select(pop + offspring, mu)
        # print(gen)
        record = stats.compile(pop)
        logbook.record(gen=gen, **record)
        print(logbook.stream)
        print(time.time() - t)

    return pop


if __name__ == '__main__':
    # simulating grid search
    # MU = [100, 200, 300]
    # CXPB = [0.9, 0.8, 0.7]
    # MUTPB = [0.1, 0.15, 0.2]
    #
    # model = XOMO.pre_defined()[3]
    #
    # for mu in MU:
    #     for cxpb in CXPB:
    #         for mutpb in MUTPB:
    #             print(mu, cxpb, mutpb),
    #             action(model, mu, 10000//mu, cxpb, mutpb)
    pass
