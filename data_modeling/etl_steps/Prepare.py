
class PreparerArtists(Preparer):
    """
    A preparer class for the artists table.
    """

    def prepare(self, values):
        return values[["artist_id", "artist_name", "artist_location",
                       "artist_latitude", "artist_longitude"]]\
            .rename({"artist_name": "name",
                     "artist_location": "location",
                     "artist_latitude": "lattitude",
                     "artist_longitude": "longitude"}, axis=1)


class PreparerSongplaysStaging(Preparer):
    """
    A preparer class for the songplays table.
    """

    def prepare(self, values):
        prepared_values = values[values["page"] == "NextSong"]
        prepared_values = prepared_values[
            ["ts", "userId", "level", "sessionId", "location", "userAgent",
             "song", "artist", "length"]]
        prepared_values.columns = ["start_time", "user_id", "level",
                                   "session_id", "location", "user_agent",
                                   "song_title", "artist_name", "song_duration"]
        return prepared_values


class PreparerUsers(Preparer):
    """
    A preparer class for the users_staging table.
    """

    def prepare(self, values):
        prepared_values = values[values["page"] == "NextSong"]
        prepared_values = prepared_values[[
            "userId", "firstName", "lastName", "gender", "level"]]
        prepared_values.columns = [
            "user_id", "first_name", "last_name", "gender", "level"]
        return prepared_values


class PreparerTime(Preparer):
    """
    A preparer class for the time table.
    """

    def prepare(self, values):
        prepared_values = values[values["page"] == "NextSong"]
        start_time = prepared_values["ts"]
        timestamp = start_time.apply(lambda x: pd.Timestamp(x, unit="ms"))
        hour = timestamp.dt.hour
        day = timestamp.dt.day
        week = timestamp.dt.week
        month = timestamp.dt.month
        year = timestamp.dt.year
        weekday = timestamp.dt.weekday
        time_values = pd.concat(
            [start_time, hour, day, week, month, year, weekday], axis=1)
        time_values.columns = ["start_time", "hour", "day", "week",
                               "month", "year", "weekday"]
        return time_values
