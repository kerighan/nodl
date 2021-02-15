from collections import Counter
from .utils import relabel
import random

@relabel
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
