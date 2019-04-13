import sys

import matplotlib.pyplot as plt
import random
import networkx as nx
import numpy as np
from matplotlib import cm as cmx


def generate_circuit(nodes):
    # gr1 = nx.connected_watts_strogatz_graph(nodes, 5, 0.5)
    # gr2 = nx.connected_watts_strogatz_graph(nodes, 5, 0.5)
    gr = nx.complete_graph(nodes)  # nx.disjoint_union(gr1, gr2)
    gr.add_edge(nodes - 1, nodes)
    for (u, v) in gr.edges():
        gr.edges[u, v]['weight'] = random.randint(5, 20)
        gr.edges[u, v].update(loops=[], voltage=None, current=None)
    apply_voltage(gr, 0, nodes - 2, 10)
    return gr


def show(gr):
    # pos = nx.spectral_layout(gr, dim=2)
    pos = nx.spring_layout(gr, k=3 / (len(gr.nodes()) ** (1 / 2)), scale=2.0)
    # nx.draw(gr, pos, node_size=30)
    attrs = nx.get_edge_attributes(gr, 'current')
    # Set Edge Color based on weight
    edges, labels = zip(*attrs.items())

    nx.draw_networkx(gr, pos, edgelist=edges,  # width=[d['current'] for _, _, d in gr.edges(data=True)],
                     edge_color=labels,
                     node_size=10,
                     edge_cmap=cmx.Reds,
                     font_size=8,
                     draw_labels=False
                     )

    # map a dict to format number values
    # attrs = {k: "{:.2f}A / {}Ω / {:.2f}V".format(v, gr.edges[k]['weight'], gr.edges[k]['voltage']) for k, v in
    #          attrs.items()}
    attrs = {k: "{:.2f}A".format(v) for k, v in attrs.items()}
    nx.draw_networkx_edge_labels(gr, pos, edge_labels=attrs, font_size=5, alpha=0.5)
    plt.axis('off')
    plt.show()


def add_edge(gr, f, t, w=random.randint(5, 20)):
    """
     If graph has an existing edge, we either have to:
      a) calculate surrogate resistance, or
      b) add an artificial edge
      c) use dimultigraphs and rewrite this whole program

     We will choose the first option, but that will hide current flow
     through other resistors between the vertices
     The second option is as easy to implement,
     just add dummy vertex and two edges, one with resistance
    """
    if gr.has_edge(f, t):
        e = gr.edges[f, t]
        if e['weight'] is None:
            # might be voltage source
            e['weight'] = w
        else:
            # surrogate resistance
            e['weight'] = e['weight'] * w / (e['weight'] + w)
    else:
        gr.add_edge(f, t, loops=[], voltage=None, current=None, weight=w)
    return gr.edges[f, t]


def apply_voltage(gr, f, t, v):
    if gr.has_edge(f, t):
        gr.edges[f, t]['voltage'] = v
    else:
        gr.add_edge(f, t, loops=[], voltage=v, current=None, weight=0)


def solve(circuit):
    """
    Use mesh analysis
    """
    meshes = nx.cycle_basis(circuit)

    res = np.zeros(len(meshes))

    # assign loop no to each edge
    for i, mesh in enumerate(meshes):
        mesh = [*mesh, mesh[0]]
        for f, t in zip(mesh[:-1], mesh[1:]):
            if circuit.edges[f, t]['voltage'] is not None:
                res[i] = circuit.edges[f, t]['voltage']

            # (f,t) is current flow vector (from f, to t)
            circuit.edges[f, t]['loops'].append((i, (f, t)))

    lin = np.zeros((len(meshes), len(meshes)))

    # perform mesh analysis
    for i, mesh in enumerate(meshes):
        mesh = [*mesh, mesh[0]]
        for f, t in zip(mesh[:-1], mesh[1:]):
            for loop, vec in circuit.edges[f, t]['loops']:
                lin[i][loop] += (1 if vec == (f, t) else -1) * circuit.edges[f, t]['weight']

    loop_currents = np.linalg.solve(lin, res)

    # calculate current flow for each resistor
    to_remove = []
    for (u, v) in circuit.edges():
        current = sum([(1 if vec == (u, v) else -1) * loop_currents[i] for i, vec in circuit.edges[u, v]['loops']])
        to_remove.append((v, u) if current > 0 else (u, v))
        edge = circuit.edges[u, v]
        edge['current'] = abs(current)
        edge['voltage'] = edge['voltage'] if edge['voltage'] is not None else edge['weight'] * current

    # make graph directed and
    circuit = circuit.to_directed(as_view=False)

    for u, v in to_remove:
        circuit.remove_edge(u, v)
    return loop_currents, circuit


def verify(gr, eps=10e-6):
    """
    Check if graph currents were correctly calculated
    :param gr: graph to check
    :return: Bool
    """

    for node in gr.nodes():
        current_in = sum([gr.edges[in_edge]['current'] for in_edge in gr.in_edges(node)])
        current_out = sum([gr.edges[in_edge]['current'] for in_edge in gr.out_edges(node)])

        if abs(current_in - current_out) > eps:
            return False

    return True


if __name__ == "__main__":
    crc = None
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            edges = [[int(f), int(t), int(w)] for f, t, w in [line.split(' ') for line in f.readlines()]]
            vertices = set()
            for v1, v2, _ in edges:
                vertices.add(v1)
                vertices.add(v2)

            vf, vt, v = edges[-1]
            edges = edges[:-1]
            crc = nx.empty_graph(len(vertices))
            [add_edge(crc, f, t, w) for f, t, w in edges]
            apply_voltage(crc, vf, vt, v)
    else:
        crc = generate_circuit(100)

    _, graph = solve(crc)
    assert verify(graph)
    show(graph)
