"""Flask configuration."""
from os import environ, path

POSTGRES_NAME = environ.get('POSTGRES_NAME')
POSTGRES_READER = environ.get('POSTGRES_READER')
POSTGRES_PW = environ.get('POSTGRES_PW')
POSTGRES_URL = f"postgresql://{POSTGRES_READER}:{POSTGRES_PW}@db:5432/{POSTGRES_NAME}"
