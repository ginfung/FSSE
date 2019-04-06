from __future__ import division
from math import sqrt, exp
import random
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


def bin_dominate(ind1, ind2):
    """
    Args:
        ind1:
        ind2:
    ALL VALUES ARE LESS IS MORE!!!!
    Returns: whether ind1 dominates ind2, i.e. True if ind1 is better than ind2
    """
    f1 = tuple(ind1.fitness.values)
    f2 = tuple(ind2.fitness.values)

    for i, j in zip(f1, f2):
        if i > j:
            return False

    if f1 == f2:
        return False
    return True


def sway(pop, evalfunc, splitor, better):
    def cluster(items):
        # print(len(items))
        # add termination condition here
        if len(items) < 100:
            return items
            #  end at here

        west, east, west_items, east_items = splitor(items)
        return cluster(west_items)

        if type(west) is list:
            map(evalfunc, west)
            map(evalfunc, east)
        else:
            evalfunc(west)
            evalfunc(east)

        if better(east, west):
            selected = east_items
        if better(west, east):
            selected = west_items
        if not better(east, west) and not better(west, east):
            selected = random.sample(west_items+east_items, len(items)//2)
            # return cluster(east_items) + cluster(west_items)
        # selected = west_items[:len(west_items)//2]+east_items[:len(east_items)//2]
        return cluster(selected)

    res = cluster(pop)

    for i in res:
        if not i.fitness.valid:
            evalfunc(i)
    # pdb.set_trace()
    return res
