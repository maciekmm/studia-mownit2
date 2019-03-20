import math

import matplotlib.pyplot as plt
import random
import networkx as nx
import numpy as np
from matplotlib import cm as cmx


def generate_circuit(nodes, threshold=0.9):
    gr = nx.connected_watts_strogatz_graph(nodes, 3, 0.5)
    for (u, v) in gr.edges():
        gr.edges[u, v]['weight'] = random.randint(5, 20)
        gr.edges[u, v].update(loops=[], voltage=None, current=None)
    return gr


def show(gr):
    pos = nx.spectral_layout(gr, dim=2)
    # nx.draw(gr, pos, node_size=30)
    attrs = nx.get_edge_attributes(gr, 'current')
    # Set Edge Color based on weight
    edges, labels = zip(*attrs.items())

    nx.draw_networkx(gr, pos, edgelist=edges,  # width=[d['current'] for _, _, d in gr.edges(data=True)],
                     edge_color=labels,
                     node_size=10,
                     edge_cmap=cmx.Reds,
                     font_size=8,
                     )

    # map a dict to format number values
    attrs = {k: "{:.2f}A / {}Ω / {:.2f}V".format(v, gr.edges[k]['weight'], gr.edges[k]['voltage']) for k, v in
             attrs.items()}
    nx.draw_networkx_edge_labels(gr, pos, edge_labels=attrs, font_size=8, alpha=0.5)
    plt.axis('off')
    plt.show()


def add_edge(gr, f, t, w=random.randint(5, 20)):
    gr.add_edge(f, t, loops=[], voltage=None, current=None, weight=w)


def solve(crc):
    # mesh analysis
    meshes = nx.cycle_basis(crc)

    # convert to directed graph, so we can assign loop
    # crc = crc.to_directed(as_view=False)
    res = np.zeros(len(meshes))

    # assign loop no to each edge
    for i, mesh in enumerate(meshes):
        mesh = [*mesh, mesh[0]]
        for f, t in zip(mesh[:-1], mesh[1:]):
            # 1 - forwards flow
            # -1 - backwards flow
            if crc.edges[f, t]['voltage'] is not None:
                res[i] = crc.edges[f, t]['voltage']

            crc.edges[f, t]['loops'].append((i, (f, t)))

    # apply voltage to first loop
    # res[2] = 10
    lin = np.zeros((len(meshes), len(meshes)))

    # perform mesh analysis
    for i, mesh in enumerate(meshes):
        mesh = [*mesh, mesh[0]]
        for f, t in zip(mesh[:-1], mesh[1:]):
            for loop, vec in crc.edges[f, t]['loops']:
                lin[i][loop] += (1 if vec == (f, t) else -1) * crc.edges[f, t]['weight']

    loop_currents = np.linalg.solve(lin, res)

    # calculate current flow for each resistor
    to_remove = []
    for (u, v) in crc.edges():
        current = sum([(1 if vec == (u, v) else -1) * loop_currents[i] for i, vec in crc.edges[u, v]['loops']])
        to_remove.append((v, u) if current > 0 else (u, v))
        edge = crc.edges[u, v]
        edge['current'] = abs(current)
        edge['voltage'] = edge['voltage'] if edge['voltage'] is not None else edge['weight'] * current

    # make graph directed and
    crc = crc.to_directed(as_view=False)

    for u, v in to_remove:
        crc.remove_edge(u, v)
    return loop_currents, crc


# crc = generate_circuit(50)
crc = nx.empty_graph(4)
# add_edge(crc, 0, 1)
# add_edge(crc, 1, 4)
# add_edge(crc, 4, 0)
# add_edge(crc, 1, 2)
# add_edge(crc, 2, 4)
# add_edge(crc, 2, 3)
# add_edge(crc, 3, 4)
# add_edge(crc, 1, 5)
# add_edge(crc, 5, 4)
# edge = random.choice(list(crc.edges))
# print(edge)
# crc.edges[edge]['voltage'] = 10
# crc.edges[edge]['weight'] = 0

add_edge(crc, 0, 3, 0)
crc.edges[0, 3]['voltage'] = 10
add_edge(crc, 0, 1, 30)
add_edge(crc, 0, 2, 30)
add_edge(crc, 1, 2, 5)
add_edge(crc, 1, 3, 10)
add_edge(crc, 2, 3, 15)

currs, graph = solve(crc)
show(graph)
