from flask import Flask
from flask import request
# from flask import render_template
from flask import jsonify
from sklearn.externals import joblib
import json
import requests
import logging as lg
from datetime import datetime as dt
from pytz import timezone
import numpy as np

app = Flask(__name__)

#     example array([[5.1, 3.5, 1.4, 0.2]])
@app.route('/api/v1.0/taxiRAP', methods=['POST'])
   
def index():
    clf = joblib.load('./trainedModels/TaxiFareRegression.pkl') # load the model
    # Fetching inputs
    query = request.get_json(silent=True, force=True)['inputs']
    X = np.array(query)

   
    # Computing predictions
    y_pred = clf.predict(X)
#     y_prob = model.predict_proba(X)

    # Building output
    output = [{"predictedTaxiFare":y_pred.tolist()}]

    # Logging predictions
    for (i,o) in zip(query, output):
        lg.info('IN | {} || OUT | {}'.format(i, o))

    return jsonify({'outputs': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
       
