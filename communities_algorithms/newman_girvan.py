import networkx as nx

from utils.plot import plot_network
from cdlib import NodeClustering


# This method keeps removing edges from Graph until one of the connected components of Graph splits into two
# compute the edge betweenness
def CmtyGirvanNewmanStep(G):
    init_ncomp = nx.number_connected_components(G)  # no of components
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')  # edge betweenness for G
        # find the edge with max centrality
        max_ = max(bw.values())
        # find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.items():
            if float(v) == max_:
                G.remove_edge(k[0], k[1])  # remove the central edge
        ncomp = nx.number_connected_components(G)  # recalculate the no of components


# This method compute the modularity of current split
def _GirvanNewmanGetModularity(G, deg_, m_):
    New_A = nx.adj_matrix(G)
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    # Let's compute the Q
    comps = nx.connected_components(G)  # list of components
    Mod = 0  # Modularity of a given partitionning
    for c in comps:
        EWC = 0  # no of edges within a community
        RE = 0  # no of random edges
        for u in c:
            EWC += New_deg[u]
            RE += deg_[u]  # count the probability of a random edge
        Mod += (float(EWC) - float(RE * RE) / float(2 * m_))
    Mod = Mod / float(2 * m_)
    return Mod


def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)  # len(A) ---> some ppl get issues when trying len() on sparse matrixes!
    B = A.sum(axis=1)
    i = 0
    for node_id in list(nodes):
        deg_dict[node_id] = B[i, 0]
        i += 1
    return deg_dict


# This method runs GirvanNewman algorithm and find the best community split by maximizing modularity measure
def runGirvanNewman(G, Orig_deg, m_):
    # let's find the best split of the graph
    BestQ = 0.0
    Q = 0.0
    while True:
        CmtyGirvanNewmanStep(G)
        Q = _GirvanNewmanGetModularity(G, Orig_deg, m_)
        if Q > BestQ:
            BestQ = Q
            Bestcomps = list(nx.connected_components(G))  # Best Split
        if G.number_of_edges() == 0:
            break
    if BestQ > 0.0:
        print("Max modularity found (Q): {} and number of communities: {}".format(BestQ, len(Bestcomps)))
        return [list(community) for community in Bestcomps]
    else:
        print("Max modularity (Q):", BestQ)


def newman_girvan(G: nx.Graph, file_name: str):
    n = G.number_of_nodes()  # |V|
    A = nx.adj_matrix(G)  # adjacenct matrix

    copy_graph = G.copy();

    m_ = 0.0  # the weighted version for number of edges
    for i in range(0, n):
        for j in range(0, n):
            m_ += A[i, j]
    m_ = m_ / 2.0

    # calculate the weighted degree for each node
    Orig_deg = {}
    Orig_deg = UpdateDeg(A, G.nodes())

    # run Newman alg
    communities = runGirvanNewman(G, Orig_deg, m_)
    if communities is None:
        # make each node a community
        communities = [[node] for node in G.nodes()]

    clustering = NodeClustering(list(communities), copy_graph)

    colors = plot_network(copy_graph, clustering, False, False, f"images/{file_name}.png")
    print(file_name, " done")
    return clustering.communities, colors
