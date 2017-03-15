from __future__ import division
from XOMO_Base.xomo_liaison import xomol
from deap import base, creator, tools
import array
import random
import pdb


class XOMO(object):
    def __init__(self, name, specific_bounds, obj_bound):
        self.name = name
        # Should be as xomol.names to maintain order of LOWs and UPs
        names = ["aa", "sced", "cplx", "site", "resl", "acap", "etat", "rely",
             "Data", "prec", "pmat", "aexp", "flex", "pcon", "tool", "time",
             "stor", "docu", "b", "plex", "pcap", "kloc", "ltex", "pr",
             "ruse", "team", "pvol"]
        # Generic Bounds as per menzies.us/pdf/06xomo101.pdf fig.9
        common_bounds = {"aa" : (1,6),
                  "sced" : (1.00,1.43),
                 "cplx" : (0.73,1.74),
                 "site" : (0.80, 1.22),
                 "resl" : (1.41,7.07),
                 "acap" : (0.71,1.42),
                 "etat" : (1,6),
                 "rely" : (0.82,1.26),
                 "Data" : (0.90,1.28),
                 "prec" : (1.24,6.20),
                 "pmat" : (1.56,7.80),
                 "aexp" : (0.81,1.22),
                 "flex" : (1.01,5.07),
                 "pcon" : (0.81,1.29),
                 "tool" : (0.78,1.17),
                 "time" : (1.00,1.63),
                 "stor" : (1.00,1.46),
                 "docu" : (0.81,1.23),
                 "b" : (3,10),
                 "plex" : (0.85,1.19),
                 "pcap" : (0.76,1.34),
                 "kloc" : (2,1000),
                 "ltex" : (0.84,1.20),
                 "pr" : (1,6),
                 "ruse" : (0.95,1.24),
                 "team" : (1.01,5.48),
                  "pvol" : (0.87,1.30)}

        self.bound = dict()
        for n in names:
            if n in specific_bounds:
                self.bound[n] = specific_bounds[n]
            else:
                self.bound[n] = common_bounds[n]

        for key, val in self.bound.items():
            if min(val) == max(val):
                self.bound[key] = (min(val), max(val)+0.000001)  # avoid divide-by-zero error

        creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
        creator.create('Individual', array.array, typecode='d', fitness=creator.FitnessMin)

        self.decsNum = len(names)
        self.decs = names
        self.obj_bound = obj_bound

        self.creator = creator
        self.Individual = creator.Individual

        self.toolbox = base.Toolbox()
        self.toolbox.register('evaluate', self.eval_ind)
        self.eval = self.toolbox.evaluate

    def eval_ind(self, ind, normalized=True):
        # demoralize the ind
        dind = []
        for dn, v in zip(self.decs, ind):
            m, M = self.bound[dn]
            dind.append(v * (M-m) + m)

        xomoxo = xomol()
        output = xomoxo.run(dind)

        if not normalized:
            ind.fitness.values = output
        else:
            noutput = list()
            for (m, M), v in zip(self.obj_bound, output):
                if v > M:
                    noutput.append(1)
                else:
                    noutput.append((v-m)/(M-m))
            ind.fitness.values = noutput

        return ind.fitness.values

# bounds specific to osp model

bounds_osp = { "prec": (4.96, 6.2),
               "flex": (1.01, 4.05),
               "resl": (4.24, 7.07),
               "team": (3.29, 4.38),
               "pmat": (3.12, 7.8),
               "rely": (1.26, 1.26),
               "cplx": (1.34, 1.74),
               "Data": (1, 1),
               "ruse": (0.95, 1.07),
               "time": (1, 1.63),
               "stor": (1, 1.17),
               "pvol": (0.87, 0.87),
               "acap": (1, 1.19),
               "pcap": (1, 1),
               "pcon": (1, 1.12),
               "aexp": (1, 1.1),
               "plex": (1, 1),
               "ltex": (0.91, 1.09),
               "tool": (1, 1.09),
               "sced": (1, 1.43),
               "site": (1, 1),
               "docu": (0.91, 1.11),
               "kloc": (75, 125)}
bounds_osp2 = {"prec": (1.24, 3.72),
                       "flex": (3.04, 3.04),
                       "resl": (2.83, 2.83),
                       "team": (3.29, 3.29),
                       "pmat": (1.56, 3.12),
                       "rely": (1.26, 1.26),
                       "cplx": (1.34, 1.74),
                       "Data": (1.14, 1.14),
                       "ruse": (0.95, 1.07),
                       "time": (1, 1),
                       "stor": (1, 1),
                       "pvol": (1, 1),
                       "acap": (0.85, 1.19),
                       "pcap": (1, 1),
                       "pcon": (1, 1.12),
                       "aexp": (0.88, 1.1),
                       "plex": (0.91, 1),
                       "ltex": (0.84, 1.09),
                       "tool": (0.78, 1.09),
                       "sced": (1, 1.14),
                       "site": (0.8, 1),
                       "docu": (1, 1.11),
                       "kloc": (75, 125)}
bounds_ground = {"prec": (1.24, 6.2),
                         "flex": (1.01, 5.07),
                         "resl": (1.41, 7.07),
                         "team": (1.01, 5.48),
                         "pmat": (1.56, 7.8),
                         "rely": (0.82, 1.1),
                         "cplx": (0.73, 1.17),
                         "Data": (0.9, 1),
                         "ruse": (0.95, 1.24),
                         "time": (1, 1.11),
                         "stor": (1, 1.05),
                         "pvol": (0.87, 1.3),
                         "acap": (0.71, 1),
                         "pcap": (0.76, 1),
                         "pcon": (0.81, 1.29),
                         "aexp": (0.81, 1.1),
                         "plex": (0.91, 1.19),
                         "ltex": (0.91, 1.2),
                         "tool": (1.09, 1.09),
                         "sced": (1, 1.43),
                         "site": (0.8, 1.22),
                         "docu": (0.81, 1.23),
                         "kloc": (11, 392)}
bounds_flight = {"prec": (6.2, 1.24),
                         "flex": (5.07, 1.01),
                         "resl": (7.07, 1.41),
                         "team": (5.48, 1.01),
                         "pmat": (6.24, 4.68),
                         "rely": (1, 1.26),
                         "cplx": (1, 1.74),
                         "Data": (0.9, 1),
                         "ruse": (0.95, 1.24),
                         "time": (1, 1.11),
                         "stor": (1, 1.05),
                         "pvol": (0.87, 1.3),
                         "acap": (1, 0.71),
                         "pcap": (1, 0.76),
                         "pcon": (1.29, 0.81),
                         "aexp": (1.22, 0.81),
                         "plex": (1.19, 0.91),
                         "ltex": (1.2, 0.91),
                         "tool": (1.09, 1.09),
                         "sced": (1, 1),
                         "site": (1.22, 0.8),
                         "docu": (0.81, 1.23)}
# objs_bound_osp = [[0, 1.1e4], [0, 80], [0, 1.5e5], [0, 12]]
# objs_bound_osp2 = [[0, 1.1e4], [0, 80], [0, 1.5e5], [0, 10]]
# objs_bound_groud = [[0, 1.2e4], [0, 80], [0, 1.3e5], [0, 11]]
# objs_bound_flight = [[0, 1.2e4], [0, 80], [0, 1.5e5], [0, 10]]
objs_bound = [[0, 8e3], [0, 65], [0, 1.3e5], [0, 10]]


def pre_defined():
    XOMO_OSP = XOMO('osp', bounds_osp, objs_bound)
    XOMO_OSP2 = XOMO('osp2', bounds_osp2, objs_bound)
    XOMO_GROUND = XOMO('ground', bounds_ground, objs_bound)
    XOMO_FLIGHT = XOMO('flight', bounds_flight, objs_bound)
    return XOMO_OSP, XOMO_OSP2, XOMO_GROUND, XOMO_FLIGHT

if __name__ == '__main__':
    model = pre_defined()[2]
    for _ in range(50):
        ind = model.Individual([random.random() for _ in range(model.decsNum)])
        print(model.eval(ind, False))