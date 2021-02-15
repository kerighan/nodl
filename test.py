import networkx as nx
from nodl.community import label_propagation
from nodl.plot import draw
import matplotlib.pyplot as plt


G = nx.karate_club_graph()

labels = label_propagation(G)
draw(G, labels)
plt.show()
