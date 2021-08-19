from flask import Flask, request

import src.models
import settings
from src.database_manager import Database
from src.movie_manager import add_new_movie, get_movies, delete_movie_by_name, update_movie_details

database = Database()

app = Flask(__name__)


@app.route('/') 
def index():
    return {"message": "Server is running"}


@app.route('/add_new_movie', methods=['POST'])
def insert_new_movie():
    """
    This is a view for adding new movies to the database.
    :return:
    """
    movie_name = request.form.get('movie_name')
    locations = request.form.get('locations').split(",")
    timings = request.form.get('timings').split(",")
    return add_new_movie(movie_name, locations, timings)


@app.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    """
    This is a view function for getting all the movies according on the search.
    :return:
    """
    location = request.args.get('location')
    timing = request.args.get('timing')
    return get_movies(location=location, timing=timing)


@app.route('/update_movie_details/<string:movie_name>', methods=['PUT'])
def edit_movie_details(movie_name):
    """
    This is a view function for update movie details.
    """
    updated_movie_name = request.form.get('updated_name')
    locations = request.form.get('locations')
    timings = request.form.get('timings')
    locations = locations.split(',') if locations else []
    timings = timings.split(',') if timings else []
    return update_movie_details(movie_name, updated_movie_name, locations=locations, timings=timings)


@app.route('/delete_movie/<string:movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    """
    This is a view function for delete movie api.
    """
    return delete_movie_by_name(movie_name)


@app.route('/recreate_tables')
def recreate_tables():
    all_tables = (src.models.Movies, src.models.MovieLocations, src.models.MovieTimings)
    database.db.drop_tables(all_tables)
    database.db.create_tables(all_tables)
    return {"status": "success", "message": "Tables recreated successfully"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.SERVER_PORT, debug=False)
