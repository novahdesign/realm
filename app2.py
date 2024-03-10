from flask import Flask, render_template
# from passageidentity import Passage, PassageError

import cohere
from flask import Flask, request, render_template_string, redirect, url_for
import pandas as pd
import joblib

app = Flask(__name__)

def return_prediction(model, input_df):
    print('input: ', input_df)
    prediction = model.predict(input_df)[0]
    return prediction

model = joblib.load('ovulationpredictor.joblib')

# Assume you have your Cohere API key stored in an environment variable or securely
cohere_api_key = '6Fdzo9FxYHFeQD8emNGOQRv292P5mAoMm8dy8Hyq'
co = cohere.Client(cohere_api_key)
PASSAGE_APP_ID= 'v2jbtAXbi7gF6tIDH0oMvBw0'
# app = Flask(__name__)

# def return_prediction(model, input_df):
#     prediction = model.predict(input_df)[0]
#     return prediction

# model = joblib.load('ovulationpredictor.joblib')


@app.route("/")
def index():
    # return render_template('index.html', psg_app_id=PASSAGE_APP_ID)
    # Adding internal CSS with improved aesthetics and a simple text-based logo
    # return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

    form_html = """
    <html>
    <div class="form-container">  
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
        
    result_template = """
    <html>
        <head>
            <title>Prediction Result</title>
        </head>
        <body>
            <h1>Prediction Result</h1>
            <p>The predicted result is: {{ prediction }}</p>

            <h1>Enter current day of cycle</h1>

            <!-- Add a form to post the prediction to the /cohere_process route -->

            <form action="/cohere_process" method="post">
                    <input type="hidden" name="prediction" value="{{ prediction }}">
                    <label for="currentDay">Current Day of Cycle:</label>
                    <input type="number" id="currentDay" name="current_day_of_cycle" min="1" required>
                    <input type="submit" value="Process with Cohere">
            </form>

        </body>
    </html>
    """
    return render_template_string(result_template, prediction=prediction)

@app.route('/cohere_process', methods=["POST"])
def process_with_cohere():
    co = cohere.Client('6Fdzo9FxYHFeQD8emNGOQRv292P5mAoMm8dy8Hyq')
    prediction = request.form.get('prediction')
    current_day_of_cycle = request.form.get('current_day_of_cycle')

    days_until_ovulation = float(prediction) - float(current_day_of_cycle)
    # Define a conversation history, assuming the context and the user's question
    # Adjust this according to your application's context and requirements
    chat_history = [
        {"role": "SYSTEM", "message": f"The day of ovulation from beginning of cycle prediction result is {prediction}."},
        {"role": "USER", "message": "Based on this prediction, what advice can you give?"}
    ]

    # Use Cohere's chat API to simulate a conversation
    response = co.chat(
        # chat_history=chat_history,
        # message=f"Given I am on day {current_day_of_cycle} of my cycle, and the predicted ovulation day is {prediction}, what should I consider?",
        message=f"Given I am {days_until_ovulation} days away from the beginning of ovulation, what should I consider?",

        # message=f"Please provide insights based on the prediction. This number is the day of ovulation from the beginning of my cycle. What should I do for my physical health? just tips, not real {prediction}.",
        connectors=[{"id": "web-search"}]
    )
    
    generated_text = response
    
    # Return a response page with the generated content
    response_template = """
    <html>
        <head><title>Cohere Response</title></head>
        <body>
            <h1>Response from Cohere</h1>
            <p>Generated text: {{ generated_text }}</p>
        </body>
    </html>
    """
    return render_template_string(response_template, generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/cohere_process', methods=["POST"])
# def process_with_cohere():
#     prediction = request.form.get('prediction')
    
#     # Use Cohere's API to process the prediction
#     response = co.generate(
#         prompt=f'Based on the prediction {prediction}, what insights can be derived?',
#         model='llm=cohere_chat_model',
#         max_tokens=50
#     )
    
#     generated_text = response.generations[0].text
    
#     # Return a response page with the generated content
#     response_template = """
#     <html>
#         <head><title>Cohere Response</title></head>
#         <body>
#             <h1>Response from Cohere</h1>
#             <p>Generated text: {{ generated_text }}</p>
#         </body>
#     </html>
#     """
#     return render_template_string(response_template, generated_text=generated_text)

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/cohere_process', methods=["POST"])
# def process_with_cohere():
#     prediction = request.form.get('prediction')
#     # Here, you would add your specific interaction with the Cohere API
#     # For example, generating text based on the prediction
#     response = co.generate(prompt=f'Based on the prediction {prediction}, as date of ovulation, what should i do', model='large', max_tokens=50)
#     # generated_text = response.generations[0].text

#     # For now, just return a simple confirmation page
#     # return f'Processed prediction: {prediction} with Cohere.'
#     return f'Processed prediction: {response} with Cohere. with {predition}'


# if __name__ == '__main__':
#     app.run(debug=True)




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

# from flask import Flask, render_template

# import cohere
# from flask import Flask, request, render_template_string, redirect, url_for
# import pandas as pd
# import joblib

# app = Flask(__name__)

# def return_prediction(model, input_df):
#     print('input: ', input_df)
#     prediction = model.predict(input_df)[0]
#     return prediction

# model = joblib.load('ovulationpredictor.joblib')

# # Assume you have your Cohere API key stored in an environment variable or securely
# cohere_api_key = '3iXzI59cWInuThfTefBEVrgZbJuEAKrAB5PU2VSY'
# co = cohere.Client(cohere_api_key)

# # app = Flask(__name__)

# # def return_prediction(model, input_df):
# #     prediction = model.predict(input_df)[0]
# #     return prediction

# # model = joblib.load('ovulationpredictor.joblib')


# @app.route("/")
# def index():
#     return render_template('index.html')
#     # Adding internal CSS with improved aesthetics and a simple text-based logo
#     form_html = """
#     <html>
#     <div class="form-container">  
#     </div>
#     <head>
#         <title>Ovulation Prediction Service</title>
#         <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
#         <style>
#             body {
#                 font-family: 'Roboto', sans-serif;
#                 background-color: #f4f4f4;
#                 margin: 0 auto;
#                 padding: 20px;
#                 max-width: 600px;
#             }
#             h1 {
#                 color: #333;
#                 text-align: center;
#             }
#             .logo {
#                 text-align: center;
#                 font-size: 24px;
#                 line-height: 1.5;
#                 color: #4CAF50;
#             }
#             label {
#                 margin-top: 20px;
#                 margin-bottom: 5px;
#                 font-weight: 500;
#             }
#             input[type="text"], input[type="submit"] {
#                 width: 100%;
#                 padding: 10px;
#                 margin-bottom: 10px;
#                 border-radius: 5px;
#                 border: 1px solid #ccc;
#                 box-sizing: border-box;
#             }
#             input[type="submit"] {
#                 background-color: #4CAF50;
#                 color: white;
#                 font-weight: 500;
#                 border: none;
#                 cursor: pointer;
#                 transition: background 0.3s ease;
#             }
#             input[type="submit"]:hover {
#                 background-color: #45a049;
#             }
#         </style>
#     </head>
#     <body>
#     <div class="logo">
#         * * * * * *<br>
#         * Ovulation *<br>
#         * Predictor *<br>
#         * * * * * *
#     </div>
#     <h1>Welcome to our ovulation prediction service! Enter your details below.</h1>
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
#         form_html += f'<label for="{field}">{field}:</label>'
#         form_html += f'<input type="text" id="{field}" name="{field}">'

#     # Close the form with a submit button and the rest of the HTML
#     form_html += """
#     <input type="submit" value="Predict">
#     </form>
#     </body>
#     </html>
#     """
    
#     return form_html

# @app.route('/predict', methods=["POST"])
# def ovulation_prediction():
#     # Ensure the request is POST
#     if request.method == "POST":
#         # Extract form data
#         input_data = {field: request.form.get(field, type=str) for field in request.form}
#         input_df = pd.DataFrame([input_data])

#         # Define numeric fields and convert them
#         numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
#                           'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
#                           'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
#                           'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
#                           'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
#                           'MensesScoreDaySix']
#         for field in numeric_fields:
#             input_df[field] = pd.to_numeric(input_df[field], errors='coerce')

#         # Predict
#         prediction = model.predict(input_df)[0]
        
#     result_template = """
#     <html>
#         <head>
#             <title>Prediction Result</title>
#         </head>
#         <body>
#             <h1>Prediction Result</h1>
#             <p>The predicted result is: {{ prediction }}</p>
#             <!-- Form to get current day of cycle and process with Cohere -->
#             <form action="/cohere_process" method="post">
#                 <input type="hidden" name="prediction" value="{{ prediction }}">
#                 <label for="currentDay">Current Day of Cycle:</label>
#                 <input type="number" id="currentDay" name="current_day_of_cycle" required>
#                 <input type="submit" value="Process with Cohere">
#             </form>
#         </body>
#     </html>
#     """
#     return render_template_string(result_template, prediction=prediction)

# @app.route('/cohere_process', methods=["POST"])
# def process_with_cohere():
#     co = cohere.Client('3iXzI59cWInuThfTefBEVrgZbJuEAKrAB5PU2VSY')

#     prediction = request.form.get('prediction')
#     current_day_of_cycle = request.form.get('current_day_of_cycle')  # Retrieve the value from the form

#     days_until_ovualation = prediction - current_day_of_cycle

#     # Define a conversation history, assuming the context and the user's question
#     # Adjust this according to your application's context and requirements
#     chat_history = [
#         {"role": "SYSTEM", "message": f"The day of ovulation from beginning of cycle prediction result is {prediction}."},
#         {"role": "USER", "message": "Based on this prediction, what advice can you give?"}
#     ]

#     # Use Cohere's chat API to simulate a conversation
    
#     # response = co.chat(
#     #     chat_history=chat_history,
#     #    message=f"Please provide insights based on the prediction. This number is the day of ovulation from the beginning of my cycle. What should I do for my physical health? just tips, not real {prediction}.",
#     #     connectors=[{"id": "web-search"}]
#     # )

#     response = co.chat(
#         model="command",
#         message=f"What should I do for my physical health if I am {prediction} days away from ovulation",
#         documents=[
#           #  {"title": "Tall penguins", "snippet": "Emperor penguins are the tallest."},
#           #  {"title": "Penguin habitats", "snippet": "Emperor penguins only live in Antarctica."},
#             {"title": "The_Effect_of_the_Menstrual_Cycle_on_Exercise_Metabolism_Implications_for_Exercise_Performance_in_Eumenorrhoeic_Women", "snippet": "Oestrogen’s stimulation and progesterone’s antagonizm of growth hormone response to exercise,[71] however, suggest oestrogen may stimulate lipolysis, but consideration of the E/P ratio in the LP would be prudent. Animal research presents convincing evidence to suggest that oestrogen can in fact increase lipolytic rate during exercise. For example, Beniot et al.[72] reported a heightened sensitivity to catecholamines in oestrogen-supplemented rats, with a corresponding increase in hormone-sensitive lipase activity. These authors suggest that oestrogen acts via its catechol-oestrogen derivative to potentiate the lipolytic action of adrenaline (epinephrine) by competing with catecholamines for catecholO-methyltransferase.[72] In addition, Hansen et al.[73] demonstrated an increase in lipolysis and reduced fatty acid synthesis in isolated fat cells from oestrogen-treated rats, while progesterone had no effect compared with control/ unsupplemented rats. Oestrogen supplementation in male rats has also been found to alter lipoprotein lipase (LPL) activity in a tissue-specific fashion.[74] While adipocyte LPL activity was reduced, muscle LPL activity was increased, promoting a redistribution of lipids from adipose to muscle tissue. Consequently, oestrogen supplementation not only elevated resting intramuscular lipid content but also promoted triacylglycerol esterification during submaximal exercise in the red vastus muscle, as triacylglycerol content was even greater post-exercise than at rest.[74] Therefore, whole body glycerol kinetics would not be able to elucidate oestrogen’s tissue-specific action but instead presents the overall summated response. However, it must be considered that interspecies differences may occur in the regulation of lipid metabolism.[75] Encouraged by the overwhelming evidence from animal studies, future studies should consider tissue-specific glycerol kinetics using methods such as arteriovenous balance during exercise in various menstrual phases including the LF phase, occurring approximately 2 days before ovulation and in which oestrogen peaks. 2.2.2 Plasma Free Fatty Acid Kinetics and Oxidation FFA Ra provides an index of plasma FFA availability and measures the release of fatty acids that are primarily derived from the hydrolysis of adipose tissue triacylglycerol into plasma.[69] When used as a measure of lipolytic response, FFA Ra does not account for triacylglycerol re-esterification.[76] FFA Rd measures the rate of uptake into tissues and has been used as an estimate of plasma FFA oxidation rate;[77] however, this is a crude estimate as the actual proportion of FFA uptake that is oxidized can vary and has been reported to be as low as 50%. [78] A number of studies have considered plasma FFA kinetics,[79-81] dietary FFA uptake into body stores[82] and plasma triacylglycerol kinetics[81] between menstrual phases,[79,81,82] and with and without oestrogen supplements in postmenopausal women[80] at rest. All studies reported no differences between menstrual phases or treatments. In fact, a similar FFA Ra at rest between menstrual phases is not surprising, as animal studies confirm that basal lipolysis is unchanged or even suppressed in the presence of oestrogen compared with oestrogen deficiency.[52,83] Conversely, oestrogen enhances catecholamine sensitivity as is noted by an upregulated lipolytic response to catecholamine stimulation with oestrogen treatment.[72,83] More recently, plasma FFA kinetics and oxidation have been compared during submaximal exercise during various menstrual phases in eumenorrhoeic women.[62,63] Jacobs et al.[63] performed a longitudinal study comparing plasma FFA metabolic response in the EF and ML phases and then with subsequent oral contraceptive use. Unfortunately, their menstrual phase comparison was reduced to a sample size of five, which limited the statistical power of the comparison. Considering this limitation they reported no significant differences in the rates of whole body fat oxidation, plasma FFA oxidation, non-plasma FFA oxidation or plasma FFA Menstrual Cycle, Metabolism and Performance 219 ª 2010 Adis Data Information BV. All rights reserved. Sports Med 2010; 40 (3) This material is the copyright of the original publisher. Unauthorised copying and distribution is prohibited. rate of appearance or disappearance or rate of re-esterification.[63] The average oestrogen concentration in the ML phase was a modest 311 pmol/L and the E/P ratio was fairly low, at 9. Furthermore, they failed to make use of the acetate correction factor in their calculation of plasma FFA oxidation, which is now established as necessary for more accurate estimates of plasma FFA oxidation rate.[84] The acetate correction factor accounts for the proportion of tracer-derived carbon label that is retained in the products of secondary exchange reactions that occur with tricarboxylic acid cycle intermediates instead of being released as carbon dioxide.[84] Our laboratory has observed significant variability in the acetate correction factor between menstrual phases.[85] The correction factor was lower in the ML phase compared with the EF phase.[85] We speculate that this may be associated with increased protein catabolism during exercise in the ML phase, as reported by others.[86] That is, the increased flux through transamination pathways may result in a slightly greater proportion of FFA tracer-derived carbon label isotope being retained in the products of subsidiary reactions with tricarboxylic acid cycle intermediates. Thus, in order to further increase the sensitivity of the comparison of plasma FFA oxidation rate between menstrual phases, it would be necessary to simultaneously derive the acetate correction factor and plasma FFA oxidation for each menstrual phase. Shortly following the study by Jacobs et al.,[63] a second study by Horton et al.[62] considered FFA kinetics during moderate exercise in the EF versus MF versus ML phases. The MF phase is characterized by a gradual increase in oestrogen concentration independently of progesterone. The authors found no variation in FFA Ra or Rd between menstrual phases. However, the average oestrogen concentration recorded in the MF phase of the study by Horton et al.[62] was moderate (264 pmol/L), and even the ML phase oestrogen value (393 pmol/L) was fairly modest for this menstrual phase, resulting in a low E/P ratio of 10.7. These authors, as with Jacobs et al.,[63] agreed that the magnitude of increase in oestrogen and the oestrogen increase relative to progesterone may be an important factor determining the impact of the ovarian hormones on fat metabolism. Horton et al.[62] went on to presume that variations may be noticeable in the LF or periovulatory period when oestrogen is elevated independently of progesterone. Such speculations are based on compelling evidence from animal studies. Ovariectomy reduces the activity of key enzymes in fat metabolism, i.e. carnitine palmitoyl transferase-I (CPT-I) and beta-3-hydroxyacyl-CoA dehydrogenase (b–HAD).[40] Oestrogen restores the activity of these enzymes, while progesterone inhibits these positive actions when oestrogen is at physiological concentrations.[40] However, a supraphysiological concentration of oestrogen overrides the negative effects of progesterone.[40] Interestingly, the difference in b-HAD activity with oestrogen treatment was only evident in muscle sections composed primarily of type I fibres[40] and not in sections of predominantly type II fibres.[40,52] Nonetheless, this rat model demonstrates the ability of the ovarian hormones to alter the capacity for skeletal muscle to oxidize FFAs by directly impacting on the cellular metabolic pathways. In an initial pilot study performed in our laboratory, we measured plasma palmitate Ra and Rd with a continuous infusion of 1-13C palmitate during moderate intensity exercise over 90 minutes in eumenorrhoeic women (n = 5) who were 3-hours postabsorptive (Oosthuyse and Bosch, unpublished observations). The women all completed the trial twice, once in the EF phase and then again in either the LF (or periovulatory) phase or ML phase or late luteal (LL) phase. The intention was to obtain the full range of ovarian hormones and E/P ratios that may occur during a menstrual cycle. We found that plasma palmitate Ra was highly correlated with E/P ratio (r = 0.85; p = 0.06) and was significant between plasma palmitate Rd and E/P ratio (r = 0.89; p = 0.04). A trend for a relationship between palmitate Ra, Rd and oestrogen concentration was evident. However, due to the limited sample size, no definite conclusions can be drawn. Nonetheless, this pilot study provides motivation for further investigations of exercising FFA metabolism of this kind that consider oestrogen and progesterone"}]
#     )
    
#     generated_text = response

#     # use summarize API
    
#     # Return a response page with the generated content
#     response_template = """
#     <html>
#         <head><title>Cohere Response</title></head>
#         <body>
#             <h1>Response from Cohere</h1>
#             <p>Prediction was: {{ prediction }}</p>
#             <p>Current day of cycle was: {{ current_day_of_cycle }}</p>
#             <p>Generated text: {{ generated_text }}</p>
#         </body>
#     </html>
#     """
#     return render_template_string(response_template, generated_text=generated_text)

# if __name__ == '__main__':
#     app.run(debug=True)

# # @app.route('/cohere_process', methods=["POST"])
# # def process_with_cohere():
# #     prediction = request.form.get('prediction')
    
# #     # Use Cohere's API to process the prediction
# #     response = co.generate(
# #         prompt=f'Based on the prediction {prediction}, what insights can be derived?',
# #         model='llm=cohere_chat_model',
# #         max_tokens=50
# #     )
    
# #     generated_text = response.generations[0].text
    
# #     # Return a response page with the generated content
# #     response_template = """
# #     <html>
# #         <head><title>Cohere Response</title></head>
# #         <body>
# #             <h1>Response from Cohere</h1>
# #             <p>Generated text: {{ generated_text }}</p>
# #         </body>
# #     </html>
# #     """
# #     return render_template_string(response_template, generated_text=generated_text)

# # if __name__ == '__main__':
# #     app.run(debug=True)

# # @app.route('/cohere_process', methods=["POST"])
# # def process_with_cohere():
# #     prediction = request.form.get('prediction')
# #     # Here, you would add your specific interaction with the Cohere API
# #     # For example, generating text based on the prediction
# #     response = co.generate(prompt=f'Based on the prediction {prediction}, as date of ovulation, what should i do', model='large', max_tokens=50)
# #     # generated_text = response.generations[0].text

# #     # For now, just return a simple confirmation page
# #     # return f'Processed prediction: {prediction} with Cohere.'
# #     return f'Processed prediction: {response} with Cohere. with {predition}'


# # if __name__ == '__main__':
# #     app.run(debug=True)




# # @app.route('/predict', methods=["POST"])
# # def ovulation_prediction():
# #     # Extract and process form data to get a prediction
# #     input_data = {field: request.form[field] for field in request.form}
# #     input_df = pd.DataFrame([input_data])

# #     # Convert numeric fields to float
# #     numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
# #                       'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
# #                       'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
# #                       'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
# #                       'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
# #                       'MensesScoreDaySix']
# #     for field in numeric_fields:
# #         input_df[field] = pd.to_numeric(input_df[field], errors='coerce')
    
# #     results = return_prediction(model, input_df)
    
# #     # Define and render the result page template with the prediction result
# #     result_template = """
# #     <html>
# #         <head>
# #             <title>Prediction Result</title>
# #         </head>
# #         <body>
# #             <h1>Prediction Result</h1>
# #             <p>The predicted result is: {{ prediction }}</p>
# #         </body>
# #     </html>
# #     """
# #     return render_template_string(result_template, prediction=results)

# # if __name__ == '__main__':
# #     app.run(debug=True)

# # @app.route("/")
# # def index():
# #     # Creating a string that holds HTML form with input boxes for each field
# #     form_html = """
# #     <h1>Welcome to our ovulation prediction service</h1>
# #     <form action="/predict" method="post">
# #     """
    
# #     # List of all the fields
# #     fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
# #               'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
# #               'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
# #               'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
# #               'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
# #               'MensesScoreDaySix']
    
# #     # For each field, add an input box to the form
# #     for field in fields:
# #         form_html += f'<label for="{field}">{field}:</label><br>'
# #         form_html += f'<input type="text" id="{field}" name="{field}"><br>'

# #     # Close the form with a submit button
# #     form_html += """
# #     <input type="submit" value="Predict">
# #     </form>
# #     """
    
# #     return form_html

# # @app.route('/predict', methods=["POST"])
# # def ovulation_prediction():
# #     # Extract form data
# #     input_data = {field: request.form[field] for field in request.form}
# #     input_df = pd.DataFrame([input_data])
    
# #     # Convert numeric fields to float
# #     numeric_fields = ['LengthofCycle', 'LengthofLutealPhase', 'FirstDayofHigh',
# #                       'TotalNumberofHighDays', 'TotalNumberofPeakDays', 'LengthofMenses',
# #                       'TotalMensesScore', 'Age', 'Height', 'Weight', 'Numberpreg',
# #                       'Abortions', 'BMI', 'MensesScoreDayOne', 'MensesScoreDayTwo',
# #                       'MensesScoreDayThree', 'MensesScoreDayFour', 'MensesScoreDayFive',
# #                       'MensesScoreDaySix']
# #     for field in numeric_fields:
# #         input_df[field] = pd.to_numeric(input_df[field], errors='coerce')
    
# #     # Get the prediction
# #     results = return_prediction(model, input_df)
    
# #     # Return the prediction result
# #     return jsonify(prediction=results)

# # if __name__ == '__main__':
# #     app.run(debug=True)


# # from flask import Flask, request, jsonify
# # import joblib

# # # 1. create an instance of the Flask class
# # app = Flask(__name__)

# # # 2. define a prediction function
# # def return_prediction(model, input_list):  
# #     print('input: ', input_list)
# #     input = pd.DataFrame(input_list)
# #     prediction = pipe_lr.predict(input)[0]
# #     return prediction


# # # 3. load our moment predictor model
# # model = joblib.load('ovulationpredictor.joblib')

# # # 4. set up our home page
# # @app.route("/")
# # def index():
# #     return """
# #     <h1>Welcome to our ovulation prediction service</h1>
# #     To use this service, complete your input list fields here. 
# #     </ul>
# #     """

# # # 5. define a new route which will accept POST requests and return our model predictions
# # @app.route('/predict', methods=["GET", "POST"])
# # def ovulation_prediction():
# #     content = request.json
# #     results = return_prediction(model, content['text'])
# #     return jsonify(results)

# # # 6. allows us to run flask using $ python app.py
# # if __name__ == '__main__':
# #     app.run()


# # app = Flask(__name__)

# # @app.route('/')
# # def hello_world():
# #     return 'Hello, World!'