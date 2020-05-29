"""
This module provides methods to load the raw data, prepare it and
store it in the data warehouse.
"""
from tqdm import tqdm

import sql_queries
from db import create_connection, insert
from etl_steps.prepare import PreparerSongs, PreparerArtists,\
PreparerTime, PreparerUsers, PreparerSongplaysStaging
from etl_steps.read import get_files, read_file


def process_song_file(cur, filepath):
    """
    Processes the raw song file.
    Args:
        cur: a database cursor.
        filepath: a string filepath.
    """
    # create preparers
    preparer_songs = PreparerSongs()
    preparer_artists = PreparerArtists()

    # open song file
    song_df = read_file(filepath)

    # insert artist record
    artist_data = preparer_artists.transform(song_df)
    insert(sql_queries.ARTIST_TABLE_INSERT, artist_data, cur)

    # insert song record
    song_data = preparer_songs.transform(song_df)
    insert(sql_queries.SONG_TABLE_INSERT, song_data, cur)


def process_log_file(cur, filepath):
    """
    Processes the raw log file.
    Args:
        cur: a database cursor.
        filepath: a string filepath.
    """
    # create preparers
    preparer_time = PreparerTime()
    preparer_users = PreparerUsers()
    preparer_songplays_staging = PreparerSongplaysStaging()

    # open log file
    log_df = read_file(filepath)

    # insert time data
    time_data = preparer_time.transform(log_df)
    insert(sql_queries.TIME_TABLE_INSERT, time_data, cur)

    # insert user data
    user_data = preparer_users.transform(log_df)
    insert(sql_queries.USER_TABLE_INSERT, user_data, cur)

    # insert songplay staging data
    songplay_staging_data = preparer_songplays_staging.transform(log_df)
    insert(sql_queries.SONGPLAY_STAGING_TABLE_INSERT, songplay_staging_data, cur)

    # migrate songplay staging data
    cur.execute(sql_queries.SONGPLAY_STAGING_TABLE_MIGRATE)

    # wipe songplay staging table
    cur.execute(sql_queries.SONGPLAY_STAGING_TABLE_WIPE)


def process_data(cur, conn, filepath, func):
    """
    Generic method to process data.
    Args:
        cur: a database cursor.
        conn: a database connection.
        filepath: a string filepath.
        func: a function that processes the filepath.
    """
    # get all files matching extension from directory
    all_files = get_files(filepath)

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for datafile in tqdm(all_files):
        func(cur, datafile)
        conn.commit()

def main():
    """
    Creates the connection to the database, creates the cursor,
    and processes song- and log files.
    """
    conn = create_connection("sparkifydb")
    cur = conn.cursor()

    process_data(cur, conn, filepath='../data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='../data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
