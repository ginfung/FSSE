from __future__ import division
from math import sqrt, exp
import pdb
import itertools


def _loss(f1, f2):
    return sum(exp(i - j) for i, j in zip(f1, f2)) / len(f1)


def cont_dominate(ind1, ind2):
    """

    Args:
        ind1:
        ind2:
    ALL VALUES ARE LESS IS MORE!!!!
    Returns: whether ind1 dominates ind2, i.e. True if ind1 is better than ind2
    """
    f1 = tuple(ind1.fitness.values)
    f2 = tuple(ind2.fitness.values)
    return _loss(f1, f2) < _loss(f2, f1)


def sway(pop, evalfunc, splitor, better):
    def cluster(items, out):
        print(len(items))
        west, east, west_items, east_items = splitor(items)
        if type(west) is list:
            map(evalfunc, west)
            map(evalfunc, east)
        else:
            evalfunc(west)
            evalfunc(east)

        # TODO add termination condition here
        if len(items) < 150:
            out += [items]
            return out
        # TODO end at here

        # pdb.set_trace()
        if better(east, west):
            cluster(east_items, out)
        if better(west, east):
        # else:
            cluster(west_items, out)

        return out

    res = cluster(pop, [])
    res = list(set(itertools.chain.from_iterable(res)))

    for i in res:
        if not i.fitness.valid:
            evalfunc(i)

    return res