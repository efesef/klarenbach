import unittest 
from sqlalchemy import create_engine 
import os 

class postgresTesting(unittest.TestCase): 
    """
    Class for unittests of klarenbach application. 
    Each method below is one unittest to be executed testing the core functionality
    """

    def test_connection(self):
        """
        Checks whether connection to postgres instance can be established. 
        """
        # note that locally, we need to specify host 0.0.0.0 rather than db which is the 
        # port when code is executed within docker container.
        uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:5432/{os.environ["POSTGRES_DB"]}'
        engine = create_engine(uri)
        sql = """select 1""" 
        results = engine.execute(sql).fetchone()[0]

        self.assertEqual(results, 1, "Connection to postgres database cannot be established.")

        
if __name__ == '__main__':
    unittest.main()