"""
This module provides methods to drop and re-create all tables.
"""
from sql_queries import CREATE_TABLE_QUERIES, DROP_TABLE_QUERIES
from db import create_connection


def create_database():
    """
    Creates the database and establishes the connection.
    """
    # connect to default database
    conn = create_connection("studentdb")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = create_connection("sparkifydb")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops all tables.
    """
    for query in DROP_TABLE_QUERIES:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all tables.
    """
    for query in CREATE_TABLE_QUERIES:
        cur.execute(query)
        conn.commit()


def main():
    """
    First, creates databse and establishes connection.
    Then, drops all tables and re-creates them.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
