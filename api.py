import requests
import os
import tmdbsimple as tmdb
import psycopg2
from db import run_sql

tmdb.API_KEY = os.environ["TMDB_API_KEY"]
tmdb.REQUESTS_TIMEOUT = 5  # seconds, for both connect and read


def get_data_from_tmdb(search_category, search_query):
    """
    Checks whether search_query can be matched to anything in the tmdb database.
    Depending on what we define in search_category we search for movies, series or people.
    https://github.com/celiao/tmdbsimple/tree/master/tmdbsimple
    """
    search = tmdb.Search()
    if search_category == "movies":
        response = search.movie(query=search_query)

        if response is None:
            return None
        else:
            for r in response["results"]:
                uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@db:5432/{os.environ["POSTGRES_DB"]}'
                engine = create_engine(uri,echo=True)

                sql = f"""INSERT INTO {search_category} ("movie_id", "movie_name", "release_dates", "reviews")
                      VALUES ('{r["id"]}', '{r["original_title"]}', '{r["release_date"]}', '{r["vote_average"]}') 
                      ON CONFLICT (movie_id) DO UPDATE;"""
                engine.execute(sql)
            return True
    else:
        raise ("Currently only service only looks at movies.")
