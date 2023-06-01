from process_data.build_friendships_graph import build_friendships_graph, get_cities, build_friendship_graphs_cities
from process_data.build_similarity_matrix import build_similarity_matrix
from process_data.get_db_connections import connect_to_music_db, connect_to_users_db, get_genres, get_users


def process_data():
    music_db = connect_to_music_db()
    users_details_db = connect_to_users_db()

    music_db_cursor = music_db.cursor()
    users_details_db_cursor = users_details_db.cursor()

    genres = get_genres(music_db_cursor)
    users = get_users(users_details_db_cursor)

    similarity_matrix_euclidian = build_similarity_matrix(genres, users, music_db_cursor, "euclidean")
    print("Built similarity matrix euclidean")
    similarity_matrix_cosine = build_similarity_matrix(genres, users, music_db_cursor, "cosine")
    print("Built similarity matrix cosine")
    friendship_graph_euclidian = build_friendships_graph(users_details_db_cursor)
    friendship_graph_cosine = friendship_graph_euclidian.copy()
    print("Built friendship graph without weights")
    for u, v in friendship_graph_euclidian.edges():
        # Assuming you have some logic to calculate the weight for each edge
        index_u = users.index(u)
        index_v = users.index(v)
        weight_euclidian = similarity_matrix_euclidian[index_u][index_v]
        weight_cosine = similarity_matrix_cosine[index_u][index_v]

        if weight_euclidian == 0:
            friendship_graph_euclidian.remove_edge(u, v)

        if weight_cosine == 0:
            friendship_graph_cosine.remove_edge(u, v)

        # Add the weight to the edge
        friendship_graph_euclidian.add_weighted_edges_from([(u, v, weight_euclidian)])
        friendship_graph_cosine.add_weighted_edges_from([(u, v, weight_cosine)])

    print("Built friendship graph with weights")

    # Close the cursors and database connections when you're done
    music_db_cursor.close()
    users_details_db_cursor.close()
    music_db.close()
    users_details_db.close()
    return friendship_graph_euclidian, friendship_graph_cosine, similarity_matrix_euclidian, similarity_matrix_cosine


def process_data_cities():
    music_db = connect_to_music_db()
    users_details_db = connect_to_users_db()

    music_db_cursor = music_db.cursor()
    users_details_db_cursor = users_details_db.cursor()

    genres = get_genres(music_db_cursor)
    users = get_users(users_details_db_cursor)

    cities = get_cities(users_details_db_cursor)
    friendship_graphs_euclidian = build_friendship_graphs_cities(users_details_db_cursor, cities)

    similarity_matrix_euclidian = build_similarity_matrix(genres, users, music_db_cursor, "euclidean")
    print("Built similarity matrix euclidean")

    for city in cities:
        friendship_graph_euclidian = friendship_graphs_euclidian[city]
        print("Built friendship graph without weights")
        for u, v in friendship_graph_euclidian.edges():
            # Assuming you have some logic to calculate the weight for each edge
            index_u = users.index(u)
            index_v = users.index(v)
            weight_euclidian = similarity_matrix_euclidian[index_u][index_v]

            if weight_euclidian == 0:
                friendship_graph_euclidian.remove_edge(u, v)

            # Add the weight to the edge
            friendship_graph_euclidian.add_weighted_edges_from([(u, v, weight_euclidian)])

        # iterate over all nodes and add edges to all other nodes
        for u in friendship_graph_euclidian.nodes():
            for v in friendship_graph_euclidian.nodes():
                index_u = users.index(u)
                index_v = users.index(v)
                weight_euclidian = similarity_matrix_euclidian[index_u][index_v]
                if u != v and weight_euclidian > 1.7:
                    friendship_graph_euclidian.add_weighted_edges_from([(u, v, weight_euclidian)])

        print("Built friendship graph with weights")
        friendship_graphs_euclidian[city] = friendship_graph_euclidian

    # Close the cursors and database connections when you're done
    music_db_cursor.close()
    users_details_db_cursor.close()
    music_db.close()
    users_details_db.close()
    return friendship_graphs_euclidian
