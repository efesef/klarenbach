from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
app = Flask(__name__)

db_name=os.environ.get("POSTGRES_NAME")
db_reader=os.environ.get("POSTGRES_READER")
db_pw=os.environ.get("POSTGRES_PW")

PG_URL=f"postgresql://{db_reader}:{db_pw}@db:5432/{db_name}"

@app.route('/')
def homepage(): 
   return(PG_URL)
 
if __name__ == "__main__": 
    app.run(debug=True)