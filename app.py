from flask import Flask, request, render_template
import json

import src.models
import settings
from src.database_manager import Database
from src.movie_manager import add_new_movie, get_movies, delete_movie_by_name, update_movie_details

database = Database()

app = Flask(__name__)



@app.route('/docs', methods=['GET'])
def get_docs():
    return render_template('swaggerui.html')


@app.route('/add_new_movie', methods=['POST'])
def insert_new_movie():
    """
    This is a view for adding new movies to the database.
    :return:
    """
    movie_name = request.form.get('movie_name')
    locations_and_timings = request.form.get('locations_and_timings')
    none_values = []
    if not movie_name:
        none_values.append("movie_name")
    if not locations_and_timings:
        none_values.append("locations_and_timings")
    if none_values:
        return {"status": "failure", "message": f'{none_values} are required params'}
    try:
        locations_and_timings = json.loads(locations_and_timings)
    except json.JSONDecodeError:
        locations_and_timings = eval(locations_and_timings)
    except Exception as e:
        return {"status": "failure", "message": f'Unexpected error occured : {e}'}
    return add_new_movie(movie_name, locations_and_timings)


@app.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    """
    This is a view function for getting all the movies according on the search.
    :return:
    """
    movie_name = request.args.get('movie_name')
    location = request.args.get('location')
    timing = request.args.get('timing')
    return get_movies(movie_name=movie_name, location=location, timing=timing)


@app.route('/update_movie_details/<string:movie_name>', methods=['PUT'])
def edit_movie_details(movie_name):
    """
    This is a view function for update movie details.
    :return:
    """
    updated_movie_name = request.form.get('updated_name')
    new_locations_and_timings = request.form.get('new_locations_and_timings')
    if new_locations_and_timings:
        try:
            new_locations_and_timings = json.loads(new_locations_and_timings)
        except json.JSONDecodeError:
            new_locations_and_timings = eval(new_locations_and_timings)
        except Exception as e:
            return {"status": "failure", "message": f'Unexpected error occurred : {e}'}
    return update_movie_details(movie_name, updated_movie_name, new_locations_and_timings)


@app.route('/delete_movie/<string:movie_name>', methods=['DELETE'])
def delete_movie(movie_name: str):
    """
    This is a view function for delete movie api.
    :return:
    """
    return delete_movie_by_name(movie_name)


@app.route('/migrate')
def migrate():
    """
    This function is used to create all the tables in the database.
    :return:
    """
    if settings.DROP_TABLES:
        print("Going to Drop tables...")
        database.db.drop_tables((src.models.Movies, src.models.MovieLocationsWithTimings))
        print("Tables dropped successfully")
    print("Going to create tables")
    database.db.create_tables((src.models.Movies, src.models.MovieLocationsWithTimings))
    print("Tables created successfully")
    return {"status": "success", "message": "Tables created successfully"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.SERVER_PORT, debug=False)
    # app.run()
