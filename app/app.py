from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import os
import psycopg2

app = Flask(__name__)


@app.route("/") 
def homepage():
    """
    Default view of flask web application.
    """
    # connect to postgres database.
    conn = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="db",
        port="5432",
    )
    cur = conn.cursor()
    sql = """SELECT count(1) FROM umwelt_panels;"""
    cur.execute(sql)
    results = cur.fetchall()
    conn.commit()
    conn.close()
    return results


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
