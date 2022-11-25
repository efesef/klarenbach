import pandas as pd
import os
from sqlalchemy import create_engine, text
import tmdbsimple as tmdb
import requests
import logging

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


def run_sql(sql):
    """
    Runs sql based on db setup.
    """
    uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_DB"]}'
    engine = create_engine(uri, echo=True)

    results = pd.read_sql(text(sql), con=engine)
    return results


def check_in_db(table_name, column_name, search_query):
    """Check if movie already exists in our db.
    Returns true if movie can be found in db (according to a lazy regex comparison).
    Returns false if not.
    """
    sql = (
        f"""SELECT * FROM {table_name} where {column_name} ilike '%{search_query}%';"""
    )
    results = run_sql(sql)
    return results.shape[0] >= 1


def get_data_from_db(table_name, column_name, search_query):
    """Check if movie already exists in our db.
    Returns none if movie is not in db.
    Returns all movies and all information from table movies if we have any matches.
    """

    sql = (
        f"""SELECT * FROM {table_name} where {column_name} ilike '%{search_query}%';"""
    )
    results = run_sql(sql)

    if results.shape[0] >= 1:
        return results.to_html()
    else:
        return None


def tmdb_to_postgres(search_category, search_query):
    """
    Checks whether search_query can be matched to anything in the tmdb database.
    Depending on what we define in search_category we search for movies, series or people.
    https://github.com/celiao/tmdbsimple/tree/master/tmdbsimple
    """

    tmdb.API_KEY = os.environ["TMDB_API_KEY"]
    tmdb.REQUESTS_TIMEOUT = 5  # seconds, for both connect and read

    search = tmdb.Search()
    if search_category == "movies":
        response = search.movie(query=search_query)

        if response is None:
            return None
        else:
            for r in response["results"]:
                uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_DB"]}'
                engine = create_engine(uri, echo=True)

                sql = f"""INSERT INTO {search_category} ("movie_id", "movie_name", "release_dates", "reviews")
                      VALUES ('{r["id"]}', '{r["original_title"]}', '{r["release_date"]}', '{r["vote_average"]}') 
                      ON CONFLICT (movie_id) DO NOTHING;"""
                try:
                    engine.execute(sql)
                except Exception as err:
                    logging.error(err, exc_info=True)
            return True
    else:
        raise ("Currently only service only looks at movies.")
