from flask import Flask, render_template
from passageidentity import Passage, PassageError

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import joblib

import os

PASSAGE_APP_ID = os.environ.get("PASSAGE_APP_ID")
PASSAGE_API_KEY = os.environ.get("PASSAGE_API_KEY")





app = Flask(__name__)

def return_prediction(model, input_df):
    print('input: ', input_df)
    prediction = model.predict(input_df)[0]
    return prediction

model = joblib.load('ovulationpredictor.joblib')

# app = Flask(__name__)

# def return_prediction(model, input_df):
#     prediction = model.predict(input_df)[0]
#     return prediction

# model = joblib.load('ovulationpredictor.joblib')


@app.route("/")
def index():
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)
    # Adding internal CSS with improved aesthetics and a simple text-based logo
    form_html = """
    <html>
    <div class="form-container">  
    <passage-auth app-id="{{psg_app_id}}"></passage-auth>
    <script src="https://cdn.passage.id/passage-web.js"></script> 
    </div>
    <head>
        <title>Ovulation Prediction Service</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f4f4f4;
                margin: 0 auto;
                padding: 20px;
                max-width: 600px;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .logo {
                text-align: center;
                font-size: 24px;
                line-height: 1.5;
                color: #4CAF50;
            }
            label {
                margin-top: 20px;
                margin-bottom: 5px;
                font-weight: 500;
            }
            input[type="text"], input[type="submit"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                font-weight: 500;
                border: none;
                cursor: pointer;
                transition: background 0.3s ease;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
    <div class="logo">
        * * * * * *<br>
        * Ovulation *<br>
        * Predictor *<br>
        * * * * * *
    </div>
    <h1>Welcome to our ovulation prediction service! Enter your details below.</h1>
    <form action="/predict" method="post">
    """
    
    # List of all the fields
    fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
              'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
              'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
              'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
              'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
              'MensesScoreDaySix']
    
    # For each field, add an input box to the form
    for field in fields:
        form_html += f'<label for="{field}">{field}:</label>'
        form_html += f'<input type="text" id="{field}" name="{field}">'

    # Close the form with a submit button and the rest of the HTML
    form_html += """
    <input type="submit" value="Predict">
    </form>
    </body>
    </html>
    """
    
    return form_html

@app.route('/predict', methods=["POST"])
def ovulation_prediction():
    # Ensure the request is POST
    if request.method == "POST":
        # Extract form data
        input_data = {field: request.form.get(field, type=str) for field in request.form}
        input_df = pd.DataFrame([input_data])

        # Define numeric fields and convert them
        numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
                          'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
                          'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
                          'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
                          'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
                          'MensesScoreDaySix']
        for field in numeric_fields:
            input_df[field] = pd.to_numeric(input_df[field], errors='coerce')

        # Predict
        prediction = model.predict(input_df)[0]
        
        # Define and render the result page template with the prediction result
        result_template = """
        <html>
            <head>
                <title>Prediction Result</title>
            </head>
            <body>
                <h1>Prediction Result</h1>
                <p>The predicted result is: {{ prediction }}</p>
            </body>
        </html>
        """
        return render_template_string(result_template, prediction=prediction)

        # return result_template

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/predict', methods=["POST"])
# def ovulation_prediction():
#     # Extract and process form data to get a prediction
#     input_data = {field: request.form[field] for field in request.form}
#     input_df = pd.DataFrame([input_data])

#     # Convert numeric fields to float
#     numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
#                       'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
#                       'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
#                       'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
#                       'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
#                       'MensesScoreDaySix']
#     for field in numeric_fields:
#         input_df[field] = pd.to_numeric(input_df[field], errors='coerce')
    
#     results = return_prediction(model, input_df)
    
#     # Define and render the result page template with the prediction result
#     result_template = """
#     <html>
#         <head>
#             <title>Prediction Result</title>
#         </head>
#         <body>
#             <h1>Prediction Result</h1>
#             <p>The predicted result is: {{ prediction }}</p>
#         </body>
#     </html>
#     """
#     return render_template_string(result_template, prediction=results)

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route("/")
# def index():
#     # Creating a string that holds HTML form with input boxes for each field
#     form_html = """
#     <h1>Welcome to our ovulation prediction service</h1>
#     <form action="/predict" method="post">
#     """
    
#     # List of all the fields
#     fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
#               'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
#               'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
#               'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
#               'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
#               'MensesScoreDaySix']
    
#     # For each field, add an input box to the form
#     for field in fields:
#         form_html += f'<label for="{field}">{field}:</label><br>'
#         form_html += f'<input type="text" id="{field}" name="{field}"><br>'

#     # Close the form with a submit button
#     form_html += """
#     <input type="submit" value="Predict">
#     </form>
#     """
    
#     return form_html

# @app.route('/predict', methods=["POST"])
# def ovulation_prediction():
#     # Extract form data
#     input_data = {field: request.form[field] for field in request.form}
#     input_df = pd.DataFrame([input_data])
    
#     # Convert numeric fields to float
#     numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
#                       'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
#                       'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
#                       'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
#                       'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
#                       'MensesScoreDaySix']
#     for field in numeric_fields:
#         input_df[field] = pd.to_numeric(input_df[field], errors='coerce')
    
#     # Get the prediction
#     results = return_prediction(model, input_df)
    
#     # Return the prediction result
#     return jsonify(prediction=results)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import joblib

# # 1. create an instance of the Flask class
# app = Flask(__name__)

# # 2. define a prediction function
# def return_prediction(model, input_list):  
#     print('input: ', input_list)
#     input = pd.DataFrame(input_list)
#     prediction = pipe_lr.predict(input)[0]
#     return prediction


# # 3. load our moment predictor model
# model = joblib.load('ovulationpredictor.joblib')

# # 4. set up our home page
# @app.route("/")
# def index():
#     return """
#     <h1>Welcome to our ovulation prediction service</h1>
#     To use this service, complete your input list fields here. 
#     </ul>
#     """

# # 5. define a new route which will accept POST requests and return our model predictions
# @app.route('/predict', methods=["GET", "POST"])
# def ovulation_prediction():
#     content = request.json
#     results = return_prediction(model, content['text'])
#     return jsonify(results)

# # 6. allows us to run flask using $ python app.py
# if __name__ == '__main__':
#     app.run()


# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'