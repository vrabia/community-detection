import numpy as np


def build_music_preferences_matrix(music_db_cursor, users, genres):
    initial_matrix = [[0 for _ in range(len(genres))] for _ in range(len(users))]
    for i in range(len(users)):
        music_db_cursor.execute("""
           SELECT GENRE, COUNT(*) FROM SONGS INNER JOIN
           LISTENED_SONGS LS on SONGS.ID = LS.SONG_ID WHERE LS.USER_ID = %s
           GROUP BY GENRE
           """, (users[i],))
        user_genres_db_data = music_db_cursor.fetchall()
        user_genres = [genre[0] for genre in user_genres_db_data]
        user_genres_count = [genre[1] for genre in user_genres_db_data]
        for j in range(len(genres)):
            if genres[j] in user_genres:
                initial_matrix[i][j] = user_genres_count[user_genres.index(genres[j])]

    row_sums = [sum(row) for row in initial_matrix]

    # Normalize the matrix by dividing each element by its row sum and multiplying by 100
    return [[(value / row_sum) * 100 if row_sum != 0 else 0 for value in row] for row, row_sum in
            zip(initial_matrix, row_sums)]


def build_similarity_matrix(genres, users, music_db_cursor, criteria):
    normalized_matrix = build_music_preferences_matrix(music_db_cursor, users, genres)
    preferences_matrix = np.array(normalized_matrix)

    match criteria:
        case "euclidean":
            from scipy.spatial.distance import euclidean
            matrix = [[euclidean(pref1, pref2) for pref2 in preferences_matrix] for pref1 in preferences_matrix]
            max_distance = np.max(matrix)
            similarity_matrix_euclidian = 2 - (matrix / max_distance)
            return similarity_matrix_euclidian
        case "cosine":
            from sklearn.metrics.pairwise import cosine_similarity
            matrix = cosine_similarity(preferences_matrix)
            similarity_matrix_cosine = 1 + matrix
            return similarity_matrix_cosine
        case _:
            raise ValueError("Invalid criteria")
