import networkx as nx

from utils.plot import plot_network


def run_infomap(friendships_graph: nx.Graph, file_name: str):
    from cdlib import algorithms
    coms = algorithms.infomap(friendships_graph)
    colors = plot_network(friendships_graph, coms, False, False, f"images/{file_name}.png")
    return coms.communities, colors
