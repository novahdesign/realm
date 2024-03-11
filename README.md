# Realm 🔮 myproj
cmd-f project slay 2024

test commit - paige

# Welcome to Realm 🔮 The reproductive wellness app

## Inspiration
We've tried and trialed various apps to help us stay on top of our cycle - but we felt something was missing. We knew that we could learn more from our cycle and how it affects our daily lives in terms of mental health, exercise and nutrition needs, and even brain activity. Research shows that menstrual cycles have an effect on many areas of our lives.

## What it does
Realm is an inclusive and informative cycle-tracking app that uses our custom-trained ML model to predict a user's current cycle phase and provide wellness tips on mental health, nutrition, exercise, and sleep.

## How we built it
### ML MODEL
We began by training our ML model using a publicly-found dataset on peoples' cycles to predict ovulation day. We preprocessed numeric features using StandardScaler() and SimpleImputer() and used sklearn Ridge to fit our model.

### COHERE API
Next, we focused on using the ovulation day data to offer health tips for users. We integrated the Cohere Retrieval Augmented Generation (RAG) API, sending it our user's predicted ovulation day, to provide timely advice related to mental health, exercise, nutrition, and more.

### 1PASSWORD PASSAGE
Finally, we integrated 1password for the login aspect of our app. We recognize that cycle data is sensitive and users should feel secure when sharing their personal information in our app. To implement this, we used the 1password Passage API and connected it to our Flask app.

## Challenges we ran into
We ran into some challenges with our integrations and understanding how to parse through the data we received to format that appropriately for the user. We also had some issues ensuring our environments were compatible while we continued to add and install new packages to support the integrations we ran.

After working together on debugging issues and problem-solving the issues with dependencies, we were able to successfully integrate our app.

## Accomplishments that we're proud of
First of all, our team is proud of our unique idea for a cycle tracking up. Realm acknowledges that understanding your cycle goes beyond just menstrual day predictions. Instead, cycle tracking can be used to support all areas of your life and help users better understand their body everyday.

Secondly, we are proud of our problem-solving ability. Dealing with many new integrations and technologies (Flask, 1password, Cohere, etc) was a challenging feat that we accomplished.

## What we learned
This was our first time working with many of these technologies. While developing our first Flask app, we learned how to make our custom-made ovulation predictor model available through an API. We also used Cohere RAG for the first time and learned how to use citations in our generated requests to help users understand the science behind our health tips. It was also our first time using the 1password integration which we learned how to implement.

## What's next for Realm
We are very passionate about this issue and think there is huge potential for more development. Feeding user data back into our ML model will improve the accuracy. Prompt engineering our requests to the Cohere API will provide more targeted advice for users. As new research on menstrual cycles becomes available, we are excited to update our app with the latest knowledge and help users use their cycle as a tool to live healthy lives.

Security-focused, AI-powered reproductive wellness.

Built With
css
flask
html
integrations
python
cohere api
1password passage
 
Devpost:

https://devpost.com/software/realm-m4hnos?ref_content=my-projects-tab&ref_feature=my_projects
