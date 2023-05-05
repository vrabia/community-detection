import random

import matplotlib.pyplot as plt
import networkx as nx
from cdlib import NodeClustering
from networkx import Graph


def plot_network(graph: Graph, coms: NodeClustering, show_node_labels: bool, show_edge_weight: bool, file_name: str):
    # Plot the graph with nodes colored by community
    pos = nx.spring_layout(graph)

    # Generate nr of communities random colors for coloring the nodes
    random.seed(42)
    num_communities = len(coms.communities)
    colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(num_communities)]

    for i, com in enumerate(coms.communities):
        nx.draw_networkx_nodes(graph, pos, nodelist=com, node_color=colors[i % len(colors)])
        if show_node_labels:
            labels = {node: node for node in com}
            nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)

    edge_labels = nx.get_edge_attributes(graph, "weight")

    if show_edge_weight:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    nx.draw_networkx_edges(graph, pos)
    plt.savefig(file_name)
    # plt.show()
