import pandas as pd
import json
import os
import psycopg2


@app.route("/")
def main():
   """ 
   Default view of flask web application. 
   """
   print("hello world")

if __name__ == "__main__":
    main()