import networkx as nx
from cdlib import algorithms

from utils.plot import plot_network

# Create a weighted graph
G = nx.karate_club_graph()

# Run the Louvain algorithm
coms = algorithms.louvain(G, weight='weight', resolution=1., randomize=False)

plot_network(G, coms, True, False, '../images/test.png')

