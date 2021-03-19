from collections import Counter
from .utils import relabel_
import random


@relabel_
def label_propagation(G, history_length=20):
    labels = {}
    # initialize communities
    for i, node in enumerate(G.nodes):
        labels[node] = i

    n_changed = float("inf")
    history = []
    nodes = list(G.nodes)
    while n_changed > 0:
        # shuffle nodes
        random.shuffle(nodes)

        # count labels changed
        n_changed = 0

        # make one pass
        for node in nodes:
            count = Counter(labels[n] for n in G.neighbors(node))
            if len(count) == 0:
                next_label = labels[node]
            elif len(count) == 1:
                next_label = count.most_common(1)[0][0]
            else:
                (max_label, max_value), (next_label, next_value) = (
                    count.most_common(2))

                if next_value != max_value:
                    next_label = max_label
                else:
                    candidates = [l for l, v in count.most_common() if v == max_value]
                    next_label = candidates[random.randint(0, len(candidates) - 1)]

            if next_label != labels[node]:
                n_changed += 1
                labels[node] = next_label

        history.append(n_changed)
        if len(history) > history_length:
            first_history = history.pop(0)
            if first_history <= n_changed + 1:
                n_changed = 0
        
    return labels


@relabel_
def infomap(G):
    import infomap as ip
    node2id = {node: i for i, node in enumerate(G.nodes)}
    id2node = {i: node for node, i in node2id.items()}

    if G.is_directed():
        infomapSimple = ip.Infomap("--two-level --directed --silent")
    else:
        infomapSimple = ip.Infomap("--two-level --silent")
    network = infomapSimple.network
    for e in G.edges:
        network.addLink(node2id[e[0]], node2id[e[1]])

    infomapSimple.run()

    c = []
    labels = {}
    for node in infomapSimple.iterTree():
        if node.isLeaf():
            node_id = node.physicalId
            module = node.moduleIndex()
            labels[id2node[node_id]] = module
    return labels


@relabel_
def louvain(G):
    import cylouvain
    return cylouvain.best_partition(G)
