import networkx as nx

from client.save_image import save_image_and_upload_html
from communities_algorithms.gacomm import community_detection as ga_community_detection
from communities_algorithms.infomap_alg import run_infomap
from communities_algorithms.louvain import louvain
from communities_algorithms.newman_girvan import newman_girvan
from communities_algorithms.spectral_clustering import run_spectral_clustering
from process_data.process_data import process_data, process_data_cities

friendship_graph_euclidian, friendship_graph_cosine, similarity_matrix_euclidian, similarity_matrix_cosine = process_data()
communities_euclidian, colors_louvain = louvain(friendship_graph_euclidian, "louvain_euclidian")
communities_cosine, colors_cosine = louvain(friendship_graph_cosine, "louvain_cosine")

save_image_and_upload_html("louvain_euclidian", communities_euclidian, colors_louvain)
save_image_and_upload_html("louvain_cosine", communities_cosine, colors_cosine)

coms, colors = run_infomap(friendship_graph_euclidian, "infomap_euclidian")
save_image_and_upload_html("infomap_euclidian", coms, colors)

coms, colors = run_infomap(friendship_graph_cosine, "infomap_cosine")
save_image_and_upload_html("infomap_cosine", coms, colors)

communities_spec_euclidian, colors_sp_eucl = run_spectral_clustering(friendship_graph_euclidian, "spectral_euclidian", 8)
communities_spec_cosine, colors_sp_cos = run_spectral_clustering(friendship_graph_cosine, "spectral_cosine", 10)

save_image_and_upload_html("spectral_euclidian", communities_spec_euclidian, colors_sp_eucl)
save_image_and_upload_html("spectral_cosine", communities_spec_cosine, colors_sp_cos)

# For Newman Girvan we need to have smaller graphs, we will process the data using the users from same cities
cities_graphs = process_data_cities()
for city, city_graph in cities_graphs.items():
    communities, colors = newman_girvan(city_graph, f"newman_girvan_euclidian{city}")
    save_image_and_upload_html(f"newman_girvan_euclidian{city}", communities, colors)

    res, colors = ga_community_detection(list(city_graph.nodes()), list(city_graph.edges()),
                                 generation=100, population=len(city_graph.nodes()),
                                 r=1.5, file_name=f"ga_community_detection{city}")
    save_image_and_upload_html(f"ga_community_detection{city}", res, colors)