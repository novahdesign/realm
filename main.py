from flask import Blueprint, render_template, g, request, jsonify, render_template_string
from passageidentity import Passage, PassageError
import pandas as pd
import joblib
import os

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

PASSAGE_APP_ID = 'v2jbtAXbi7gF6tIDH0oMvBw0'
PASSAGE_API_KEY = 'jndJqbt0NE.cnF50aSCBepyMNbOqhog01bgXOaH5EhuEIcyaK5jR0hwonWVIFJiyPCEuM2Hk9Yw'

try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as e:
    print(e)
    exit()

@auth.before_request
def before_request():
    try:
        g.user = psg.authenticateRequest(request)
    except PassageError as e:
        return render_template('unauthorized.html')

def return_prediction(model, input_df):
    prediction = model.predict(input_df)[0]
    return prediction

model = joblib.load('ovulationpredictor.joblib')

@main.route("/")
def index():
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

    # Your HTML form code...