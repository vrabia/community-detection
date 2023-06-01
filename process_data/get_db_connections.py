import os
import mysql.connector


def connect_to_users_db():
    users_details_db = mysql.connector.connect(
        host="localhost",
        port=os.getenv("USERS_DB_HOST_PORT"),
        user=os.getenv("USERS_MYSQL_USER"),
        password=os.getenv("USERS_MYSQL_PASSWORD"),
        database=os.getenv("USERS_MYSQL_DATABASE")
    )
    return users_details_db


def connect_to_music_db():
    music_db = mysql.connector.connect(
        host="localhost",
        port=os.getenv("MUSIC_DB_HOST_PORT"),
        user=os.getenv("MUSIC_MYSQL_USER"),
        password=os.getenv("MUSIC_MYSQL_PASSWORD"),
        database=os.getenv("MUSIC_MYSQL_DATABASE")
    )

    return music_db


def get_genres(music_db_cursor):
    music_db_cursor.execute("select DISTINCT GENRE from SONGS")
    genres = music_db_cursor.fetchall()
    return [genre[0] for genre in genres]


def get_users(user_details_cursor):
    user_details_cursor.execute("select DISTINCT ID from VRUSERS")
    users = user_details_cursor.fetchall()
    return [user[0] for user in users]
