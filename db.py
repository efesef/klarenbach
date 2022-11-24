import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy import text

def run_sql(sql):
    """
    Runs sql based on db setup.
    """
    uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@db:5432/{os.environ["POSTGRES_DB"]}'
    engine = create_engine(uri,echo=True)

    results = pd.read_sql(
        text(sql),
        con=engine
    )        
    return results



def check_in_db(table_name, column_name, search_query):
    """Check if movie already exists in our db.
    Returns true if movie can be found in db (according to a lazy regex comparison).
    Returns false if not.
    """
    sql = f"""SELECT count(1) FROM {table_name} where {column_name} ilike '%{search_query}%';"""
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
