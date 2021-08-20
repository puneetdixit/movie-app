import peewee

from src.database_manager import Database

database = Database()


class Movies(peewee.Model):
    movie_id = peewee.PrimaryKeyField(constraints=[peewee.SQL('AUTO_INCREMENT')])
    movie_name = peewee.CharField(unique=True)

    class Meta:
        database = database.db
        db_table = 'movies'


class MovieLocationsWithTimings(peewee.Model):
    movie_id = peewee.ForeignKeyField(Movies, on_delete='CASCADE')
    location = peewee.CharField()
    timing = peewee.TimeField()

    class Meta:
        database = database.db
        db_table = 'movie_locations_and_timings'
        indexes = (
            (('movie_id', 'location', 'timing'), True),
        )