# -*- coding: utf-8 -*-

import random
from .util import id_generator

template_structure ="""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
<key attr.name="topic" attr.type="string" for="edge" id="topic" />
<graph edgedefault="directed">
{NODES}
{EDGES}
</graph>
</graphml>
"""

template_node = '<node id="{node_id}"/>'

template_edge = '<edge id="{edge_id}" directed="true" source="{from_node}" target="{to_node}"> <data key="topic">{topic}</data> </edge>'


def _convert_line(line):
    """Ignore comments(#)  and strip values from columns"""
    if not line.strip() or line.startswith('#'):
        return None, None
    from_node, to_node = line.split()
    return from_node.strip(), to_node.strip()


def convert_tsv_into_graphml(input_file, output_file, topics):
    nodes = set()
    edges = []
    edge_id_gen = id_generator()

    for line in input_file.readlines():
        from_node, to_node = _convert_line(line)
        if from_node is None:
            continue
        nodes.add(from_node)
        nodes.add(to_node)
        edges.append((from_node, to_node))

    node_lines = '\n'.join(template_node.format(node_id=id) for id in nodes)
    edge_lines = '\n'.join(template_edge.format(from_node=f,
                                                to_node=t,
                                                edge_id=edge_id_gen.next(),
                                                topic=random.choice(topics)) for f, t in edges)
    with open(output_file, 'wb') as out_fd:
        out_fd.write(template_structure.format(NODES=node_lines, EDGES=edge_lines))
