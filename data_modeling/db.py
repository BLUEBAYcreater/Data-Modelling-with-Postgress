"""
This module provides methods to interact with the database.
"""
import psycopg2

import settings


def create_connection(database, user_name=None, user_password=None,
                      host="127.0.0.1"):
    """
    Creates a connection to a database.
    """
    if user_name is None:
        user_name = settings.DB_USER_NAME
    if user_password is None:
        user_password = settings.DB_USER_PASSWORD
    connection_dict = {
        "host": host,
        "user_name": user_name,
        "user_password": user_password,
        "database": database
    }
    return psycopg2.connect(
        "host={host} dbname={database} \
        user={user_name} password={user_password}".format(**connection_dict))


def insert(query, records, cur):
    """
    Inserts all records with query in cursor.
    """
    for record in records:
        cur.execute(query, record)
