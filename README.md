# movie-app
This is a backend server for movie-app in Python3 language using Flask Framework. MySql as a 
Database and Peewee ORM to communicate with the database.

To connect with database change in settings.py file accordingly.
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USERNAME = "root"
    DB_PASSWORD = "abc@321"
    DB_NAME = "movies_data

    These are my credentials and where my database is hosted.

This server is serving on Google Cloud Platform (GCP) https://movie-app-323508.el.r.appspot.com/ You can test it. Just 
replace http://127.0.0.1:5000/ with above url.

You have are trying to run this on your machine, migrate data to your database using this API http://127.0.0.1:5000/migrate

1. To view movies, timings, location
    This is a GET method.

    -> http://127.0.0.1:5000/get_all_movies to get all the movies without any filter.

    You can use single and multiple filters (movie_name, timing, location) on this api it will give you result accordingly.
    Example: 

    -> http://127.0.0.1:5000/get_all_movies?location=delhi&timing=13:00&movie_name=abcd

2. To add new movie to the movie list.
    This is a POST method.

    -> http://127.0.0.1:5000/add_new_movie?
    Provide data for movie in form-data format.
    movie_name: str
    locations_and_timings: dict

    Example:
        movie_name = ABCD
        locations_and_timings = {
            "Delhi": ["11:00", "12:00", "13:00", "14:00"],
            "Mumbai": ["10:30", "11:45", "14:30"],
            "Ahmedabad: ["10:15", "11:15"]
        }
        
        In the locations_and_timings fields all the keys are locations and all the values are timings.

3. To edit a movie name, timings and, locations.
    This is a PUT method.
    -> http://127.0.0.1:5000/update_movie_details/{movie_name}

    Provide the updated movie details in form-data format.
    updated_name: str
    new_locations_and_timings: dict

    Example:
        http://127.0.0.1:5000/update_movie_details/ABCD

        updated_name = XYZ
        new_locations_and_timings = {
            "Ahmedabad: ["14:15", "16:15"]
        }

        In the new_locations_and_timings fields all the keys are locations and all the values are timings.
        It will change the movie name from ABCD to XYZ and delete all old locations and timings and add timings in
        Ahmedabad location.
        You can change movie name or locations_and_timings separately.

4. To delete a movie from list.
    This is a DELETE method.

    -> http://127.0.0.1:5000/delete_movie/{movie_name}

    Example:
        If you want to delete a movie named with ABCD
        http://127.0.0.1:5000/delete_movie/ABCD