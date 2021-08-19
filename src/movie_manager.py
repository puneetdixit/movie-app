from src.models import Movies, MovieLocations, MovieTimings
import peewee


def add_new_movie(movie_name: str, locations: list, timings: list):
    """
    This function is used to insert new movie details into their respective tables.
    :param movie_name:
    :param locations: list of locations
    :param timings: list of timings
    :return:
    """
    try:
        movie_id = Movies.insert(movie_name=movie_name).execute()
    except peewee.IntegrityError:
        return {"status": "error", "message": "Movie already exists"}

    try:    
        for location in locations:
            MovieLocations.insert(movie_id=movie_id, location=location).execute()
        for timing in timings:
            MovieTimings.insert(movie_id=movie_id, timing=timing).execute()
    except Exception as e:
        print("Error inserting locations or timings : ", str(e))
    return {"status": "success", "message": movie_name + " added successfully" }


def get_movies(timing=None, location=None):
    """
    This function is used to get the movies from the database based on timing and location filter.
    :param timing:
    :param location:
    :return:
    """
    if location and timing:
        result = Movies.select(Movies.movie_name, MovieLocations.location, MovieTimings.timing)\
            .join(MovieLocations).dicts().switch(Movies).join(MovieTimings).dicts()\
            .where(MovieLocations.location == location, MovieTimings.timing == timing).execute()
    elif location:
        result = Movies.select(Movies.movie_name, MovieLocations.location, MovieTimings.timing)\
            .join(MovieLocations).dicts().switch(Movies).join(MovieTimings).dicts()\
            .where(MovieLocations.location == location).execute()
    elif timing:
        result = Movies.select(Movies.movie_name, MovieLocations.location, MovieTimings.timing)\
            .join(MovieLocations).dicts().switch(Movies).join(MovieTimings).dicts()\
            .where(MovieTimings.timing == timing).execute()
    else:
        result = Movies.select(Movies.movie_name, MovieLocations.location, MovieTimings.timing)\
            .join(MovieLocations).dicts().switch(Movies).join(MovieTimings).dicts().execute()
    
    return {"status": "success", "data": [row for row in result]}


def update_movie_details(movie_name, updated_name=None, timings=None, locations=None):
    """
    This Function is used to update the movie details.
    :param movie_name:
    :param updated_name:
    :param timings:
    :param locations:
    :return:
    """
    try:
        movie_id = Movies.get(Movies.movie_name==movie_name).movie_id
    except peewee.DoesNotExist:
        return {"status": "failure", "message": f'{movie_name} dose not exits in the system'}

    if updated_name:
        Movies.update(movie_name=updated_name).where(Movies.movie_id == movie_id).execute()

    if timings:
        print(f'updated timing {timings} for {movie_name}')
        MovieTimings.delete().where (MovieTimings.movie_id==movie_id).execute()
        for timing in timings:
            MovieTimings.insert(movie_id=movie_id, timing=timing).execute()
    
    if locations:
        print(f'updated locations {locations} for {movie_name}')
        MovieLocations.delete().where (MovieLocations.movie_id==movie_id).execute()
        for location in locations:
            MovieLocations.insert(movie_id=movie_id, location=location).execute()

    return {"status": "success", "message": f'{movie_name} details updated successfully'}


def delete_movie_by_name(movie_name):
    """
    This function is used to delete the movie by name.
    :param movie_name:
    :return:
    """
    try:
        Movies.get(Movies.movie_name == movie_name).delete_instance()
        return {"status": "success", "message": f'{movie_name} deleted successfully'}    
    except peewee.DoesNotExist:
        return {"status": "failure", "message": f'{movie_name} dose not exits in database'}
    except Exception as e:
        return {"status": "failure", "message": f'Error in deleting movie {movie_name} {e}'}
