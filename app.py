from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def homepage():
   df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
   })
   fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('plotly.html', graphJSON=graphJSON)

if __name__ == "__main__": 
    app.run(debug=True, host='0.0.0.0', port=5001)