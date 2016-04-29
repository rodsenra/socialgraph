# -*- coding: utf-8 -*-

import random
import itertools
import networkx as nx
from .util import invert_dict, all_pairwise_combinations

# Make reproducible random choices
random.seed(123)


def elect_committee(original_G, max_members, max_iter=100):
    """
    Identifies a committee in graph original_G with no more than max_members.
    :param original_G: The social networkx instance graph.
    :param max_members: the number of members in the committee.
    :param max_iter: limit to the number of iterations in the algorithm.
    :return:
    """
    iteration = 0
    committee = {}
    G = original_G.copy()
    while len(committee) < max_members:
        iteration += 1
        all_candidates, support_base = compute_powers(G)
        candidate = select_candidate(G, all_candidates)
        base = support_base[candidate]
        committee[candidate] = base
        G.remove_nodes_from(base)
        if iteration > max_iter:
            raise Exception('Maximum iteration limit reached while electing committee.')
    return committee


def compute_powers(G):
    """
    Computes two dictionaries:
      * powers -> key==node, value==delegation power of node
      * support_base -> key==node, value==all nodes represented by the key node.

    Complexity |V|**2 * complexity(has_path).
    has_path could be implemented to be O(V+E), using DFS with adjancency lists.
    """
    support_base = {}
    V = G.nodes()
    powers = dict(zip(V, [0]*len(V)))
    for dst in V:
        for src in V:
            if nx.has_path(G, src, dst):
                powers[dst] += 1
                try:
                    support_base[dst].append(src)
                except KeyError:
                    support_base[dst] = [src]

    return powers, support_base


def select_candidate(G, candidate_dict):
    power_dict = invert_dict(candidate_dict)
    top_voting = max(power_dict.keys())
    top_candidates = power_dict[top_voting]
    if len(top_candidates) == 1:
        candidate = top_candidates[0]
    else:
        candidate = (random.choice(top_candidates)
                     if independent_nodes(G, top_candidates)
                     else candidate_from_depedent_tie(G, top_candidates))

    return candidate


def candidate_from_depedent_tie(G, dependent_candidates):
    aux_G = G.copy()
    dependent_edges = all_pairwise_combinations(dependent_candidates)
    for v,u in dependent_edges:
        try:
            aux_G.remove_edge(v, u)
        except nx.NetworkXError:
            pass
    all_candidates, support_base = compute_powers(aux_G)
    return select_candidate(aux_G, all_candidates)


def independent_nodes(G, node_list):
    return not any(nx.has_path(G, i, j) for i, j in all_pairwise_combinations(node_list))


def subgraph_by_topic(G, topic):
    """ Create a induced subgraph with just the edges of a given topic
    :param G: the nx Graph object
    :param topic: string with the topic label
    :return: new nx Graph with a single topic
    """
    E = []
    for edge in G.edges_iter():
        edge_attrs = G.get_edge_data(*edge)
        if edge_attrs['topic'] == topic:
            E.append(edge)

    return nx.DiGraph(E)


def paint_graph(G, committee):
    colorG = G.copy()
    represented_base = list(itertools.chain.from_iterable(committee.values()))

    committee_node_colors = {k: 'red' for k, _ in committee.items()}
    base_node_colors = {k: 'green' for k in represented_base}

    nx.set_node_attributes(colorG, 'color', base_node_colors)
    nx.set_node_attributes(colorG, 'color', committee_node_colors)
    return colorG