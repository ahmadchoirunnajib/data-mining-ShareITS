import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph(day="Friday")
G.graph
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()