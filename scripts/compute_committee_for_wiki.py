# -*- coding: utf-8 -*-

import os
import networkx as nx
from nxpd import draw
from socialgraph.socialgraph import subgraph_by_topic, elect_committee, paint_graph


MAX_EDGES = 300
TOPIC = 'Groceries'

wiki_file = os.path.join('..', 'datasets', 'wiki.graphml')

G = nx.read_graphml(wiki_file)
print("Full graph: {0} nodes {1} edges".format(len(G.nodes()), len(G.edges())))

# Generate smaller graph and override G
subnodes = G.nodes()[:MAX_EDGES]
G = G.subgraph(subnodes)
print("Subgraph: {0} nodes {1} edges".format(len(G.nodes()), len(G.edges())))

# Filter graph by subtopic
G = subgraph_by_topic(G, TOPIC)
draw(G)

committee = elect_committee(G, 20)
print("Committee:")
print({k: len(v) for k, v in committee.items()})
draw(paint_graph(G, committee))