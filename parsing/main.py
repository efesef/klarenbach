import pandas as pd
from helper import *
from sqlalchemy import create_engine

def main(): 
    """
    Function that reads local file "umweltreport_laender" and parses 
    the information from the unstructured worksheets into a pg database. 
    """
    df = pd.read_excel('umweltreport_laender.xlsx', sheet_name=None)
    # extract sheets with actual data. 
    sheets = [k for k in list(df.keys()) if re.match(r"[0-9]+.[0-9]+",k)]
    pg_uri = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@db:5432/{os.environ["POSTGRES_DB"]}'

    df_to_pg(df, sheets, pg_uri)

if __name__ == "__main__":
    main() 
