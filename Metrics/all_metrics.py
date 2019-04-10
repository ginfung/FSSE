from __future__ import division
import sys
import os
path = os.getcwd()
rootpath = path[:path.rfind('FSSE') + 4]
sys.path.append(rootpath)

from deap import creator, base
from deap.tools.emo import sortNondominated
from Metrics.hv import HyperVolume
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

# def put_record_here(filename, model):
#     def calc(PFc):
#         creator.create(
#             "FitnessMin", base.Fitness, weights=[-1.0] * len(PFc[0]))
#         creator.create("Individual", str, fitness=creator.FitnessMin)

#         pop = list()
#         for sol in PFc:
#             ind = creator.Individual(str(
#                 sol))  # a trick here... use the fitness to identify solutions
#             ind.fitness = creator.FitnessMin(sol)
#             pop.append(ind)

#         del PFc
#         PFc = pop[:]
#         del pop
#         PFc = _get_frontier(PFc)  # DEAP version
#         PFc_list = [i.fitness.values for i in PFc]  # PYTHON LIST version
#         if len(PFc) < MINIMUM_PFS:
#             return model, -1, -1, len(PFc), -1, PFc

#         # GD
#         # load the PF0
#         PF0 = list()
#         with open('./PF_0/' + model + '.txt', 'r') as f:
#             for l in f:
#                 e = l.strip('\n').split(' ')
#                 e = [float(i) for i in e]
#                 PF0.append(e)
#         gd = GD(PF0, PFc_list)

#         # GS
#         gs = GS(PF0, PFc_list)
#         # PFS
#         pfs = len(PFc)
#         # HV
#         rp = [1] * len(PFc[0].fitness.values)  # reference point

#         hv = HyperVolume(rp).compute(PFc_list)
#         hv = round(hv, 4)

#         return model, gd, gs, pfs, hv, PFc

#     with open(filename, 'r') as f:
#         content = f.readlines()
#     content = map(lambda l: l.strip('\n'), content)
#     if content[-1].startswith('~~~'):
#         content = content[:-1]

#     times = list()
#     PFc = []

#     for l in content:
#         if l.startswith('T:'):
#             times.append(float(l[2:]))
#             continue
#         if l.startswith('Gen:'):
#             continue
#         if l.startswith('~~~'):
#             PFc = []
#             continue
#         # filtering for SPL
#         e = l.split(' ')
#         e = [round(float(i), 3) for i in e]
#         if PRODUCT_LINE_ONLY:
#             if e[0] > 0.00001:
#                 continue
#             e = e[1:]
#         PFc.append(e)

#     if len(PFc) == 0:
#         pdb.set_trace()

#     model, gd, gs, pfs, hv, _ = calc(PFc)
#     return model, gd, gs, pfs, hv


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


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    models = ['osp', 'osp2', 'ground', 'flight', 'p3a', 'p3b', 'p3c']

    # for model in models:
    #     global_info(model)
    #     print(f"{model} global_info Done.")
