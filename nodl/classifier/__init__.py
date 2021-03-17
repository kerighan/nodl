import random
import networkx as nx


def relational_classifier(G, labels):
    import numpy as np

    # adjacency matrix
    A = nx.adjacency_matrix(G)
    indptr = A.indptr
    indices = A.indices
    weights = A.data

    labelset = set(labels.values())
    n_labels = len(labelset)

    node2id = {node: i for i, node in enumerate(G.nodes)}
    n_nodes = len(node2id)

    # probability matrix
    P = np.ones((n_nodes, n_labels,), dtype=np.float32) / n_labels

    # initialize training set
    for node, label in labels.items():
        node_id = node2id[node]
        P[node_id] = 0.
        P[node_id, label] = 1.

    # learn
    nodes = [node for node in G.nodes if node not in labels]
    random.shuffle(nodes)
    n_changed = float("inf")
    while n_changed > 0:
        n_changed = 0
        
        # one pass
        for node in nodes:
            node_id = node2id[node]
            
            # get neighbors ids
            start = indptr[node_id]
            end = indptr[node_id + 1]

            node_weight = 0
            probability = np.zeros((n_labels,), dtype=np.float32)
            for neighbor_id, w in zip(indices[start:end], weights[start:end]):
                probability += w * P[neighbor_id]
                node_weight += w
            probability /= node_weight

            if not np.allclose(probability, P[node_id]):
                n_changed += 1
                P[node_id] = probability
    
    results = {}
    for node, probability in zip(G.nodes, P):
        results[node] = probability
    return results


def loopy_belief_propagation(G, labels, psi):
    import numpy as np

    # on en supprime les cycles
    T = nx.minimum_spanning_tree(G)

    # définitions utiles
    n_nodes = len(T.nodes)
    node2id = {node: i for i, node in enumerate(T.nodes)}
    nodes = list(T.nodes)
    random.shuffle(nodes)

    # initialisation de notre training set
    training_nodes = set(labels.keys())
    labelset = set(labels.values())
    n_labels = len(labelset)

    # initialisation des prior
    phi = np.ones((n_nodes, n_labels)) / n_labels

    # pas d'incertitude pour les noeuds du training set :
    for node, label in labels.items():
        node_id = node2id[node]
        phi[node_id] = 0
        phi[node_id, label] = 1

    # initialisation des messages
    messages = {}
    for source, target in G.edges:
        i = node2id[source]
        j = node2id[target]
        messages[i, j] = np.ones((n_labels,), dtype=np.float32)
        messages[j, i] = np.ones((n_labels,), dtype=np.float32)

    # propagation de la conviction pour 10 itérations
    alpha = 1
    for iteration in range(2):
        for node in nodes:
            # on utilise la notation des slides pour i, j et k
            i = node2id[node]
            # estimation de l'état de j selon i
            m_i2j = psi @ phi[i]

            # on met à jour les messages envoyés à chaque voisin
            for neighbor_j in T.neighbors(node):
                j = node2id[neighbor_j]

                # on évite de changer le message des training nodes
                if node not in training_nodes:
                    # on initialise un vecteur de 1
                    # pour multiplier les messages intrants
                    m_ki = np.ones((n_labels,))
                    # on fait le produit des messages
                    for neighbor_k in T.neighbors(node):
                        if neighbor_k == neighbor_j:
                            continue

                        k = node2id[neighbor_k]
                        m_ki *= messages[k, i]
                    m_i2j *= m_ki
                # on met à jour le message
                m_i2j /= m_i2j.max()
                messages[i, j] = alpha * m_i2j

    # on obtient la probabilité d'appartenir à une classe en normalisant le belief
    for node in G.nodes:
        i = node2id[node]
        p = phi[i]
        m_ki = np.ones((n_labels,))
        for neighbor in G.neighbors(node):
            k = node2id[neighbor]
            m_ki *= messages[k, i]
        p *= m_ki
        p /= np.sum(p)  # on normalise les croyances
        phi[i] = p  # on remplace les priors par les probabilités finales

    results = {}
    for node, probability in zip(G.nodes, phi):
        results[node] = probability
    return results

