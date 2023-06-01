import networkx as nx
from cdlib import algorithms

from utils.plot import plot_network


def louvain(friendships_weighted_graph: nx.Graph, file_name: str):
    # Run the Louvain algorithm
    coms = algorithms.louvain(friendships_weighted_graph, weight='weight', resolution=1., randomize=False)

    colors = plot_network(friendships_weighted_graph, coms, False, False, 'images/' + file_name + '.png')
    return coms.communities, colors
