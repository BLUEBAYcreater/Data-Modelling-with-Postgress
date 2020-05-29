# Data Modeling Project

In this project, I have applied what I have learned on data modeling with Postgres and build an ETL pipeline using Python. 
To complete the project, you will need to define fact and dimension tables for a star schema for a particular 
analytic focus, and write an ETL pipeline that transfers data from files in two local directories 
into these tables in Postgres using Python and SQL.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The following steps are tested only for Ubuntu 18.04.

### Docker

This project comes with a docker container with PostgreSQL and the necessary user (student) and database (studentdb). To get the container up and running, please execute:

```
docker-compose up
```

### Virtual Environment

All necessary packages are listed in the ```requirements.txt``` file and can be installed by executing:

```
bin/setup
```

### Running the ETL Process

To create and populate the database, execute the following commands:

```
source env/bin/activate   # activate the virtual environment
cd data_modeling          # move into the source folder
python create_tables.py   # create database and empty tables
python etl.py             # populate tables
```

You can validate that everything went well with the following commands:
```
cd ..                    # move back to the root folder
bin/pytest               # test that all tables have been populated properly.
```

This will create a virtual environment ```env``` in your root folder.

## Data Warehousing at Sparkify

Sparkify is a music streaming startup that provides free and premium plans and aims to convert more free users to paid customers. For this purpose, they seek to get to know more about their songs, artists and especially - their customers and their usage patterns.  

Currently, Sparkify is storing the majority of their data in .json files, which is tedious to work with, inefficient when the amount of data grows and prone to data loss. Therefore, they have decided to implement a more sophisticated data warehouse and the corresponding ETL processes.

## Database Schema

The database schema follows the Snowflake style, with one fact table (songplays) and four dimension tables (time, users, songs and artists).

The songplays table has foreign key constraints to all dimensions and well as a composite primary key, made out of all foreign keys.

## ETL Processes

The implemented ETL process follows the project instructions and adds upon that by:
1. Using object-oriented programming principles to improve code efficiency and re-usability.  
2. Using a staging area for the fact table to improve INSERT statement performance.
3. Separating source code from credentials.

### Object-Oriented Preparation

The most relevant step in the ETL pipeline is to convert raw data into a format that is compatible with the database tables. This involves three steps:

1. Select relevant columns, generate new columns and rename columns.  
2. Convert all values to native data types.  
3. Convert to a list of dictionaries data structure.

For this purpose, the ```etl_steps/prepare.py``` module provides a generic ```Preparer``` class, where step 2 and 3 are already implemented. Therefore, the child classes ```PreparerSongs```, ```PreparerArtists```, ```PreparerSongplaysStaging```, ```PreparerUsers``` and ```PreparerTime``` only have to define how to complete step 1.

### Staging Area for Songplays

The ```songplays``` table contains foreign keys to the ```songs```, ```artists```, ```users``` and ```time``` table. In the case of ```songs``` and ```artists```, the foreign key needs to be retrieved from the corresponding table through a ```JOIN```.

This challenge is tackled by defining a new table ```songsplays_staging```, where the data is temporarily stored in a preliminary format. The retrieval of the forerign key values and the insertion into the ```songplays``` table therefore only happens on the database side. Afterwards, all values are wiped from the staging table. The query to migrate ```songplays_staging``` to ```songplays``` is as follows:

```
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT songplays_staging.start_time,
       songplays_staging.user_id,
       songplays_staging.level,
       songs_artists.song_id,
       songs_artists.artist_id,
       songplays_staging.session_id,
       songplays_staging.location,
       songplays_staging.user_agent
  FROM songplays_staging
  LEFT JOIN (
       SELECT songs.song_id,
              artists.artist_id,
              songs.title,
              artists.name,
              songs.duration
         FROM songs
         LEFT JOIN artists
           ON songs.artist_id = artists.artist_id)
    AS songs_artists
    ON songplays_staging.song_title = songs_artists.title
   AND songplays_staging.artist_name = songs_artists.name
   AND songplays_staging.song_duration = songs_artists.duration
 WHERE songs_artists.song_id IS NOT NULL
    ON CONFLICT DO NOTHING;
```

