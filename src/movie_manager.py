import peewee

from src.models import Movies, MovieLocationsWithTimings


def add_new_movie(movie_name: str, locations_and_timings: dict):
    """
    This function is used to insert new movie details into their respective tables.
    :param movie_name:
    :param locations_and_timings:
    :return:
    """
    try:
        movie_id = Movies.insert(movie_name=movie_name).execute()
        for location, timings in locations_and_timings.items():
            for timing in timings:
                MovieLocationsWithTimings.insert(movie_id=movie_id, location=location, timing=timing).execute()

    except peewee.IntegrityError:
        return {"status": "failure", "message": "Movie already exists in the list"}

    except Exception as e:
        return {"status": "failure", "message": f'Error inserting locations or timings : {e}'}
    return {"status": "success", "message": f'{movie_name} added successfully'}


def get_movies(movie_name=None, timing=None, location=None):
    """
    This function is used to get the movies from the database based on timing and location filter.
    :param movie_name:
    :param timing:
    :param location:
    :return:
    """
    if movie_name and location and timing:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(Movies.movie_name == movie_name,
                                                           MovieLocationsWithTimings.location == location,
                                                           MovieLocationsWithTimings.timing == timing).execute()
    elif movie_name and location:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(Movies.movie_name == movie_name, 
                                                           MovieLocationsWithTimings.location == location).execute()
    elif movie_name and timing:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(Movies.movie_name == movie_name,
                                                           MovieLocationsWithTimings.timing == timing).execute()
    elif location and timing:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(MovieLocationsWithTimings.timing == timing,
                                                           MovieLocationsWithTimings.location == location).execute()
    elif movie_name:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(Movies.movie_name == movie_name).execute()
    elif location:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(MovieLocationsWithTimings.location == location).execute()
    elif timing:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().where(MovieLocationsWithTimings.timing == timing).execute()
    else:
        result = Movies.select(Movies.movie_name, MovieLocationsWithTimings.location, MovieLocationsWithTimings.timing)\
            .join(MovieLocationsWithTimings).dicts().execute()

    data = []
    for row in result:
        row["timing"] = str(row["timing"])
        data.append(row)
    return {"status": "success", "data": data}


def update_movie_details(movie_name, updated_name=None, new_locations_and_timings=None):
    """
    This Function is used to update the movie details.
    :param movie_name:
    :param updated_name:
    :param new_locations_and_timings:
    :return:
    """
    try:
        movie_id = Movies.get(Movies.movie_name == movie_name).movie_id
    except peewee.DoesNotExist:
        return {"status": "failure", "message": f'{movie_name} dose not exits in the system'}

    if updated_name:
        Movies.update(movie_name=updated_name).where(Movies.movie_id == movie_id).execute()

    if new_locations_and_timings:
        MovieLocationsWithTimings.delete().where(MovieLocationsWithTimings.movie_id == movie_id).execute()
        for location, timings in new_locations_and_timings.items():
            for timing in timings:
                MovieLocationsWithTimings.insert(movie_id=movie_id, location=location, timing=timing).execute()
    
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
        return {"status": "failure", "message": f'{movie_name} dose not exits in movie list'}
    except Exception as e:
        return {"status": "failure", "message": f'Error in deleting movie {movie_name} {e}'}
