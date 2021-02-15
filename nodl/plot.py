import networkx as nx


def draw(G, labels):
    nx.draw(G, node_color=[labels[node] for node in G.nodes])
