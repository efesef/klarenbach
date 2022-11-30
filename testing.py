import unittest
from sqlalchemy import create_engine, text
import os
from db import run_sql, check_in_db


class postgresTesting(unittest.TestCase):
    """
    Class for unittests of klarenbach application.
    Each method below is one unittest to be executed testing the core functionality
    """

    def test_connection(self):
        """
        Checks whether connection to postgres instance can be established.
        """
        uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_DB"]}'
        engine = create_engine(uri)
        sql = """select 1"""
        results = engine.execute(sql).fetchone()[0]

        self.assertEqual(
            results, 1, "Connection to postgres database cannot be established."
        )

    def test_run_sql(self):
        """
        Test whether run_sql function works as intended.
        """
        sql = """ select movie_name,reviews from movies where movie_name = 'dummy'"""

        results = run_sql(sql)
        self.assertEqual(
            list(results.iloc[0, :]),
            ["dummy", 5],
            results,
        )

    def test_check_in_db(self):
        """
        Test whether check_in_db function works as intended
        """
        self.assertTrue(check_in_db("movies", "movie_name", "dummy"))


if __name__ == "__main__":
    unittest.main()
