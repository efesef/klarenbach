from flask import Flask, render_template, request
import pandas as pd
import json
import os
from db import *
from api import *
import logging
from sqlalchemy import create_engine


logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)
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
        logging.info(f"Searching for {form_data['movies']}", exc_info=True)

        if check_in_db("movies", "movie_name", form_data["movies"]):
            return render_template(
                "data.html",
                form_data=get_data_from_db("movies", "movie_name", form_data["movies"]),
            )
            logging.info(
                f"Movie {form_data['movies']} already existed in db", exc_info=True
            )
        else:
            try:
                logging.info(
                    f"Movie {form_data['movies']} needs to be looked up in TMDB",
                    exc_info=True,
                )
                tmdb_results = get_data_from_tmdb("movies", form_data["movies"])

                if tmdb_results == None:
                    return "Unfortunately, we cannot find your movie in TMDB either."
                    logging.info(
                        f"Movie {form_data['movies']} could not be found in TMDB",
                        exc_info=True,
                    )

                else:
                    logging.info(
                        f"Movie {form_data['movies']} will be written to TMDB and can now be queried",
                        exc_info=True,
                    )
                    return render_template(
                        "data.html",
                        form_data=get_data_from_db(
                            "movies", "movie_name", form_data["movies"]
                        ),
                    )
            except Exception as err:
                logging.error(err, exc_info=True)
                return "An error occured"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
