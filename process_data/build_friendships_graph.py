import networkx as nx


def get_cities(user_details_cursor):
    user_details_cursor.execute("""
    select DISTINCT V.CITY
    from VRUSERS inner join VRADDRESSES V on VRUSERS.ADDRESS_ID = V.ID
    group by V.CITY having COUNT(*) > 10
    """)
    cities = user_details_cursor.fetchall()
    return [city[0] for city in cities]


def build_friendship_graphs_cities(user_details_cursor, cities):
    friendship_graphs = {}
    for city in cities:
        friendship_graphs[city] = nx.Graph()

    user_details_cursor.execute("SELECT VRUSERS.ID, V.CITY FROM VRUSERS INNER JOIN VRADDRESSES V ON VRUSERS.ADDRESS_ID = V.ID")
    users_with_cities = user_details_cursor.fetchall()

    for user in users_with_cities:
        user_id, city = user
        if city not in cities:
            continue
        friendship_graphs[city].add_node(user_id)

    user_details_cursor.execute("SELECT DISTINCT LEAST(USER1, USER2) AS USER1, GREATEST(USER1, USER2) AS USER2 FROM VRFRIENDSHIPS")

    for row in user_details_cursor:
        user1, user2 = row
        # check if both users are in the same city
        city1 = None
        for user in users_with_cities:
            if user[0] == user1:
                city1 = user[1]
                break

        city2 = None
        for user in users_with_cities:
            if user[0] == user2:
                city2 = user[1]
                break

        if city1 != city2:
            continue
        if city1 is None or city2 is None:
            continue
        if city1 not in cities:
            continue
        friendship_graphs[city1].add_edge(user1, user2)

    return friendship_graphs


def build_friendships_graph(user_details_cursor):
    user_details_cursor.execute("Select ID from VRUSERS")
    friendships_graph = nx.Graph()
    users = user_details_cursor.fetchall()
    for user in users:
        friendships_graph.add_node(user[0])

    user_details_cursor.execute("""
    SELECT DISTINCT LEAST(USER1, USER2) AS USER1, GREATEST(USER1, USER2) AS USER2
    FROM VRFRIENDSHIPS 
    """)

    for row in user_details_cursor:
        user1, user2 = row
        friendships_graph.add_edge(user1, user2)

    return friendships_graph
