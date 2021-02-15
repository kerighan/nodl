from nodl.classifier import relational_classifier, loopy_belief_propagation
import matplotlib.pyplot as plt
from nodl.plot import draw
import networkx as nx
import numpy as np


G = nx.karate_club_graph()

train_labels = {
    0: 0,
    33: 1,
    31: 2
}
labels = relational_classifier(G, train_labels)

# psi = np.array([
#     [.8, .1, .1],
#     [.3, .5, .2],
#     [.3, .2, .5]
# ])
# labels = loopy_belief_propagation(G, train_labels, psi)


draw(G, labels)
plt.show()

