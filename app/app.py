from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import os 

app = Flask(__name__)

@app.route('/')
def homepage():
   return os.environ["POSTGRES_URL"]
   
if __name__ == "__main__": 
    app.run(debug=True, host='0.0.0.0', port=5001)