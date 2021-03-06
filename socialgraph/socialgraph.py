# -*- coding: utf-8 -*-

import random
import itertools
import networkx as nx
from .util import invert_dict, all_pairwise_combinations

# Make reproducible random choices
random.seed(123)


def precompute_lengths(G):
    length = {}
    for v in G.nodes():
        length[v] = nx.single_source_shortest_path_length(G, v)
    return length


def has_path(lengths, src, dst):
    try:
        return lengths[src][dst] >= 0
    except:
        return False


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
    lengths = precompute_lengths(G)
    while len(committee) < max_members:
        iteration += 1
        all_candidates, support_base = compute_powers(G, lengths)
        candidate = select_candidate(G, all_candidates, lengths)
        base = support_base[candidate]
        committee[candidate] = base
        G.remove_nodes_from(base)
        if iteration > max_iter:
            raise Exception('Maximum iteration limit reached while electing committee.')
    return committee


def compute_powers(G, lengths):
    """
    Computes the delegation powers of all nodes, returning two dictionaries:

      * powers -> key==node, value==delegation power of node
      * support_base -> key==node, value==all nodes represented by the key node.
      * lengths -> sparse matrix of path lengths

    Complexity |V|**2.
    """
    support_base = {}
    V = G.nodes()
    powers = dict(zip(V, [0]*len(V)))
    for dst in V:
        for src in V:
            if has_path(lengths, src, dst):
                powers[dst] += 1
                try:
                    support_base[dst].append(src)
                except KeyError:
                    support_base[dst] = [src]

    return powers, support_base


def select_candidate(G, candidate_dict, lengths):
    """
    Identify the next candidate.

    :param G:
    :param candidate_dict:
    :return:
    """
    power_dict = invert_dict(candidate_dict)
    top_voting = max(power_dict.keys())
    top_candidates = power_dict[top_voting]
    if len(top_candidates) == 1:
        candidate = top_candidates[0]
    else:
        candidate = (random.choice(top_candidates)
                     if independent_nodes(G, top_candidates, lengths)
                     else candidate_from_depedent_tie(G, top_candidates, lengths))

    return candidate


def candidate_from_depedent_tie(G, dependent_candidates, lengths):
    aux_G = G.copy()
    dependent_edges = all_pairwise_combinations(dependent_candidates)
    for v, u in dependent_edges:
        try:
            aux_G.remove_edge(v, u)
        except nx.NetworkXError:
            pass
    all_candidates, support_base = compute_powers(aux_G, lengths)
    valid_candidates = {k: all_candidates[k] for k in dependent_candidates}
    top_voted = invert_dict(valid_candidates)
    candidate = top_voted[max(top_voted.keys())]
    return candidate[0]


def independent_nodes(G, node_list, lengths):
    """
    Test if the nodes in node_list represent an independent base.
    :param G:
    :param node_list:
    :return: True if all nodes in node_list are independent amongst themselves.
    """
    return not any(has_path(lengths, i, j) for i, j in all_pairwise_combinations(node_list))


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
    """
    Color the committee nodes and its represented base nodes.
    """
    colorG = G.copy()
    represented_base = list(itertools.chain.from_iterable(committee.values()))

    committee_node_colors = {k: 'red' for k, _ in committee.items()}
    base_node_colors = {k: 'green' for k in represented_base}

    nx.set_node_attributes(colorG, 'color', base_node_colors)
    nx.set_node_attributes(colorG, 'color', committee_node_colors)
    return colorG