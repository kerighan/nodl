import networkx as nx
import numpy as np


def to_hex(colortuple):
    if len(colortuple) <= 2:
        colortuple = colortuple + (0,) * (3 - len(colortuple))
    return '#' + ''.join(f'{i:02X}' for i in colortuple)


def draw(G, labels, pos=None):
    sample_value = next(iter(labels.values()))

    if isinstance(sample_value, np.ndarray):
        n_labels = sample_value.shape[0]
    
        if n_labels <= 3:
            colors = []
            for node in G.nodes:
                colortuple = tuple(np.round(labels[node] * 255).astype(int))
                colors.append(to_hex(colortuple))
        nx.draw(G, node_color=colors, pos=pos)
    else:
        nx.draw(G, node_color=[labels[node] for node in G.nodes], pos=pos)
