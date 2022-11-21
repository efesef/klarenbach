import pandas as pd
import psycopg2
import os


def run_sql(sql,query_type='select'): 
    """
    Runs sql based on db setup.
    """
    conn = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="db",
        port="5432",
    )
    cur = conn.cursor()
    cur.execute(sql)
    if query_type == "select":
        results = cur.fetchall()
        conn.commit()
        conn.close()
        return results 
    else: 
        conn.commit()
        conn.close()
        return True 



def check_in_db(table, column, search_query):
    """Check if movie already exists in our db.
    Returns true if movie can be found in db (according to a lazy regex comparison).
    Returns false if not.
    """
    
    sql = f"""SELECT count(1) FROM {table} where {column} ilike '%{search_query}%';"""
    results = run_sql(sql, 'select') 

    if results[0][0] >= 1:
        return True
    else:
        return False


def get_data_from_db(table, column, search_query):
    """Check if movie already exists in our db.
    Returns none if movie is not in db.
    Returns all movies and all information from table movies if we have any matches.
    """

    sql = f"""SELECT * FROM {table} where {column} ilike '%{search_query}%';"""
    results = run_sql(sql, 'select')

    if len(results) > 0:
        return results
    else:
        return None


def get_columns_of_table(table_name):
    """
    Inputs table name and returns list of columns that can be inserted into an insert sql statement.
    """
    sql = f"""SELECT
                    column_name
                FROM
                    information_schema.columns
                WHERE
                    table_name = '{table_name}';"""
    
    results = run_sql(sql, 'select')

    if len(results) == 0 : 
        print(f"Table {table_name} cannot be found in db schema.")
    else: 
        column_string = ','.join([x[0] for x in results])
        return column_string 

print(get_columns_of_table('movies'))
print(get_data_from_db('movies','movie_name','tatort'))
print(check_in_db('movies','movie_name','tatort'))
