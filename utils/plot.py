import random

import matplotlib.pyplot as plt
import networkx as nx
from cdlib import NodeClustering
from networkx import Graph

from process_data.get_db_connections import connect_to_music_db, connect_to_users_db


def plot_network(graph: Graph, coms: NodeClustering, show_node_labels: bool, show_edge_weight: bool, file_name: str):
    # Plot the graph with nodes colored by community
    plt.figure(figsize=(10, 10), dpi=300)
    pos = nx.spring_layout(graph, k=0.4)

    # Generate nr of communities random colors for coloring the nodes
    random.seed(12345)
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

    # Generate the legend labels and handles
    legend_labels = ['Community {}'.format(i + 1) for i in range(len(coms.communities))]
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in
                      colors[:len(coms.communities)]]
    nx.draw_networkx_edges(graph, pos)

    # Add legend to the plot
    plt.legend(legend_handles, legend_labels, loc='best')
    print("Saving plot to: ", file_name)
    plt.savefig(file_name, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    return colors


def map_users(file_name, communities, colors):
    import folium

    music_connection = connect_to_music_db()
    music_db_cursor = music_connection.cursor()
    users_connection = connect_to_users_db()
    users_db_cursor = users_connection.cursor()

    users = getUsersForMap(music_db_cursor, users_db_cursor, communities)

    map_center = [46, 25]
    m = folium.Map(location=map_center, zoom_start=7.2)

    # Generate random colors for each community
    community_colors = colors

    # Plot each user as a marker with its community color
    for user in users:
        info = f"Name: {user['name']}<br>"
        info += f"Most listened genre: {user['most_listened_genre']}<br>"
        info += f"Community number: {user['community'] + 1}<br>"
        marker = folium.CircleMarker(
            location=[user["latitude"], user["longitude"]],
            radius=8,
            color=community_colors[user["community"]],
            fill=True,
            fill_color=community_colors[user["community"]],
        )
        marker.add_child(folium.Popup(info))  # Add a pop-up with the user's name
        marker.add_to(m)

    # Save the map to an HTML file
    m.save("html/" + file_name + ".html")
    music_db_cursor.close()
    users_db_cursor.close()
    music_connection.close()
    users_connection.close()


def getUsersForMap(music_db_cursor, users_db_cursor, communities):
    music_db_cursor.execute("SELECT User_id, longitude, latitude FROM LIVE_LISTENED_SONGS")
    users = music_db_cursor.fetchall()
    users = list(set(users))
    users_with_names = []
    for user in users:
        users_db_cursor.execute("SELECT name FROM VRUSERS WHERE ID = %s", (user[0],))
        name = users_db_cursor.fetchone()
        # find community
        given_community = 100
        for community in communities:
            if user[0] in community:
                given_community = communities.index(community)
                break

        if given_community == 100:
            continue

        music_db_cursor.execute("""
        SELECT GENRE, count(*) as number FROM SONGS INNER JOIN
        LISTENED_SONGS LS on SONGS.ID = LS.SONG_ID WHERE LS.USER_ID = %s
        GROUP BY GENRE ORDER BY number desc LIMIT 1
        """, (user[0],))
        most_listened_genre = music_db_cursor.fetchone()
        if most_listened_genre is not None:
            most_listened_genre = most_listened_genre[0]
        else:
            most_listened_genre = "Unknown"

        user_with_name = {
            "user_id": user[0],
            "latitude": user[2],
            "longitude": user[1],
            "name": name[0],
            "community": given_community,
            "most_listened_genre": most_listened_genre
        }
        users_with_names.append(user_with_name)
    return users_with_names
