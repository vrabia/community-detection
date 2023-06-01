from sklearn.cluster import SpectralClustering
import networkx as nx
from cdlib import NodeClustering
from utils.plot import plot_network


def run_spectral_clustering(friendships_weighted_graph: nx.Graph, file_name: str, community_number: int):
    # Create a mapping between node indices and UUIDs
    node_indices = list(friendships_weighted_graph.nodes())
    uuid_mapping = {i: node_indices[i] for i in range(len(node_indices))}

    adj_matrix = nx.to_numpy_array(friendships_weighted_graph, weight='weight')

    # Apply Spectral Clustering for community detection with weights
    model = SpectralClustering(n_clusters=community_number, affinity='precomputed', random_state=42)
    labels = model.fit_predict(adj_matrix)

    communities = []
    for i in range(community_number):
        communities.append([])

    for i, label in enumerate(labels):
        communities[label].append(uuid_mapping[i])  # Map the node index to the corresponding UUID

    clustering = NodeClustering(list(communities), friendships_weighted_graph)

    colors = plot_network(friendships_weighted_graph, clustering, False, False, f"images/{file_name}.png")

    return clustering.communities, colors
