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
    # connect to postgres database.
    conn = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    return os.environ["POSTGRES_URL"]


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
