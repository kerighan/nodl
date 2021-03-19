from collections import Counter

def relabel_(func):
    def wrapper(*args, **kwargs):
        labels = func(*args, **kwargs)
        # relabel from 0 to n by decreasing size
        return relabel(labels)
    return wrapper


def relabel(labels):
    count = Counter(labels.values())
    old2new = {}
    for i, (old_label, _) in enumerate(count.most_common()):
        old2new[old_label] = i
    labels = {node: old2new[label] for node, label in labels.items()}
    return labels
