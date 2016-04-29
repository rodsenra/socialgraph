# -*- coding: utf-8 -*-
import itertools


def id_generator(seed=0):
    """Generator to produce sequential IDs"""
    while True:
        yield seed
        seed += 1


def invert_dict(d):
    """Invert dict d[k]=v to be p[v]=[k1,k2,...kn]"""
    p = {}
    for k, v in d.items():
        try:
            p[v].append(k)
        except KeyError:
            p[v] = [k]
    return p

def select_top_k(score_dict, k):
    return list(itertools.islice(reversed(sorted((v, k) for k, v in score_dict.items())), 0, k))


def all_pairwise_combinations(node_list):
    forward = list(itertools.combinations(node_list, 2))
    backward = [(j, i) for (i, j) in forward]
    return forward + backward


