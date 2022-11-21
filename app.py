from flask import Flask, render_template, request
import pandas as pd
import json
import os
import psycopg2
from db import *
from api import * 

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("main.html")


@app.route("/data/", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/data' to submit form"
        )
    elif request.method == "POST":
        form_data = request.form

        if check_in_db('movie', 'movie_name', request.form['movie']):
            return render_template(
                "data.html",
                form_data=get_data_from_db(
                    "movie", "movie_name", request.form["movie"]
                ),
            )
        else:
            try:
                tmdb_results = get_data_from_tmdb(request.form["movie"])
                if tmdb_results == None:
                    return "Unfortunately, we cannot find your movie in TMDB either."
                else:
                    return render_template(
                        "data.html",
                        form_data=get_data_from_db(
                            "movie", "movie_name", request.form["movie"]
                        ),
                    )
            except:
                return "An error occurred. Sorry"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
