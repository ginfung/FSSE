from __future__ import division
from POM3_Base.pom3 import pom3
from deap import base, creator, tools
import array
import random
import pdb


class POM3(object):
    def __init__(self, name, specific_bounds, obj_bound):
        self.name = name
        # Should be as xomol.names to maintain order of LOWs and UPs
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism",
                 "Size", "Plan", "Team Size"]

        self.bound = dict()
        for n, l, u in zip(names, specific_bounds[0], specific_bounds[1]):
            self.bound[n] = [l, u]

        for key, val in self.bound.items():
            if min(val) == max(val):
                self.bound[key] = (min(val), max(val)+0.000001)  # avoid divide-by-zero error

        creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0, -1.0))
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
            dind.append(v * (M - m) + m)

        p3 = pom3()
        output = p3.simulate(dind)
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

# bounds specific to pom3 model
bounds_pom3a = [[0.1, 0.82, 2, 0.40, 1, 1, 0, 0, 1], [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]]
bounds_pom3b = [[0.10, 0.82, 80, 0.40, 0, 1, 0, 0, 1], [0.90, 1.26, 95, 0.70, 100, 50, 2, 5, 20]]
bounds_pom3c = [[0.50, 0.82, 2, 0.20, 0, 40, 2, 0, 20], [0.90, 1.26, 8, 0.50, 50, 50, 4, 5, 44]]
bounds_pom3d = [[0.10, 0.82, 2, 0.60, 80, 1, 0, 0, 10], [0.20, 1.26, 8, 0.95, 100, 10, 2, 5, 20]]

objs_bound = [[0, 1300], [0, 0.7], [0, 0.65]]


def pre_defined():
    POM3A = POM3('p3a', bounds_pom3a, objs_bound)
    POM3B = POM3('p3b', bounds_pom3b, objs_bound)
    POM3C = POM3('p3c', bounds_pom3c, objs_bound)
    POM3D = POM3('p3d', bounds_pom3d, objs_bound)
    return POM3A, POM3B, POM3C, POM3D


# if __name__ == '__main__':
#     model = pre_defined()[0]
#     a, b, c = list(), list(), list()
#
#     for i in range(500):
#         # print(i)
#         ind = model.Individual([random.random() for _ in range(model.decsNum)])
#         aa, bb, cc = model.eval(ind)
#         a.append(aa)
#         b.append(bb)
#         c.append(cc)
#         print(aa,bb,cc)
#     a = sorted(a)
#     b = sorted(b)
#     c = sorted(c)
#     pdb.set_trace()
