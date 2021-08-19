import peewee
from src.database_manager import Database

database = Database()

class Movies(peewee.Model):
    movie_id = peewee.PrimaryKeyField(constraints=[peewee.SQL('AUTO_INCREMENT')])
    movie_name = peewee.CharField(unique=True)

    class Meta:
        database = database.db
        db_table = 'movies'


class MovieLocations(peewee.Model):
    movie_id = peewee.ForeignKeyField(Movies, on_delete='CASCADE')
    location = peewee.CharField(unique=True)

    class Meta:
        database = database.db
        db_table = 'movie_locations'


class MovieTimings(peewee.Model):
    movie_id = peewee.ForeignKeyField(Movies, on_delete='CASCADE')
    timing = peewee.CharField()

    class Meta:
        database = database.db
        db_table = 'movie_timing'
    