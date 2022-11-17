from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def homepage():
   return app.config["POSTGRES_URL"]
   
if __name__ == "__main__": 
    app.run(debug=True, host='0.0.0.0', port=5001)