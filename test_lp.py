from nodl.community import label_propagation
import matplotlib.pyplot as plt
from nodl.plot import draw
import networkx as nx


G = nx.karate_club_graph()

labels = label_propagation(G)
draw(G, labels)
plt.show()
