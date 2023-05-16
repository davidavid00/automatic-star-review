# import necessary libraries
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
import pandas as pd
from nltk.corpus import stopwords
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
sid = SentimentIntensityAnalyzer()
from nltk.tokenize import word_tokenize

import os
from joblib import load
import warnings
warnings.filterwarnings("ignore")
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect)
# UNCOMMENT THE BELOW FOR YOUR FIRST TIME RUN
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

# import importlib

# def check_dependencies():
#     try:
#         importlib.import_module('wordcloud')
#     except ImportError:
#         install_wordcloud()

# def install_wordcloud():
#     try:
#         import pip
#     except ImportError:
#         print("pip is not installed. Please install pip and try again.")
#         return

#     try:
#         pip.main(['install', 'wordcloud'])
#     except Exception as e:
#         print("An error occurred while installing wordcloud:", e)
#         return

#     print("wordcloud successfully installed.")

# # Check if wordcloud is installed
# check_dependencies()





# os.environ["FLASK_DEBUG"] = "1"

#################################################
# Machine Learning Setup
#################################################
model = load('review_program/static/joblib/model_lr.joblib')
vectorizer = load('review_program/static/joblib/vectorizer_LR.joblib')
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Setup the emolex dataframe
emolex_df = pd.read_csv('reinier/data/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', sep='\t', names=['word', 'emotion','association'])
emolex_df = emolex_df[emolex_df.association == 1]
emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association')
emolex_words = emolex_words.reset_index()

#Filepath for image assets
dynamic_fp = os.path.abspath('review_program/static/assets/img')

# Create route that renders index.html template
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("test.html")

# Word Cloud Setup
stop_words = stopwords.words('english') + ["'ve", "'re", "'s", "'m", "'ll", "'d", "n't", "'u", "u"]



# Prediction Route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        data = request.get_data(as_text=True)  # get the input data as a string
        print('Received data:', data)
        data_vectorized = vectorizer.transform([data])  # vectorize the data
        prediction = model.predict(data_vectorized)[0]  # make a prediction
        sentiment_label = ['negative', 'neutral', 'positive'][prediction]
        return jsonify({'prediction': sentiment_label})  # return the prediction as a JSON object
    except Exception as e:
        print('Error:', e)
        return jsonify({'success': False, 'error': str(e)})


# Graphs for dashboard
@app.route('/graphs', methods=['POST'])
def get_reviews():
    reviews = request.get_json()
    json_string = json.dumps(reviews)
    json_list = json.loads(json_string)
    df = pd.json_normalize(json_list)
    print(df)

    documents = []
    for review in json_list:
        documents.append(review['text'])
    
    emotions_output = []
    for doc in documents:
        emotions_count = emolex(doc)
        emotions_output.append(emotions_count)
    emolex_df = pd.DataFrame(emotions_output)
    print(emolex_df)
    
    if emolex_df.empty:
        return jsonify({'success': False, 'message': 'No emotions found.'})
    
    ax = emolex_df.plot(kind='bar', stacked=True, figsize=(10, 6))
    ax.set_title('Emotion Counts')
    ax.set_xlabel('Emotion')
    ax.set_ylabel('Count')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(dynamic_fp, 'emotions.png'))

    #Create Wordcloud
    df['text'] = df['text'].apply(remove_part_words)
    text = ' '.join(df['text'])

    # Create and generate a word cloud image:
    wordcloud = WordCloud(background_color='white').generate(text)

    # Display the generated image
    plt.clf()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(os.path.join(dynamic_fp, 'wordcloud.png'), bbox_inches='tight')

    # Process the reviews data as needed
    return jsonify({'success': True})


# Function for removing stopwords
def remove_part_words(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Iterate through each word
    filtered_words = []
    for word in words:
        if word.lower() not in stop_words:
            if "'" in word:
                word_parts = word.split("'")
                filtered_words.append(word_parts[0])
            else:
                filtered_words.append(word.lower())
    
    # Join the filtered words back into a single string
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

# Function to be called to calculate the emotional data for graphs
def emolex(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    emotions_count = emolex_words[emolex_words.word.isin(words)].sum()
    return emotions_count

# from flask_sqlalchemy import SQLAlchemy
# 'or' allows us to later switch from 'sqlite' to an external database like 'postgres' easily
# os.environ is used to access 'environment variables' from the operating system

# IF WE WANT TO USE A DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///mydatabase.sqlite"

# Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the SQLAlchemy app to a variable
# db = SQLAlchemy(app)

#Create the model for the data
# class Bionet(db.Model):
#     __tablename__ = 'bionetNSW'

#     uuid = db.Column(db.String(64), primary_key=True)
#     animal_class = db.Column(db.String(64))
#     basisOfRecord = db.Column(db.String(64))
#     sex = db.Column(db.String(64))
#     stateConservation = db.Column(db.String(64))
#     protectedInNSW = db.Column(db.String(64))
#     eventDate = db.Column(db.String(64))
#     decimalLatitude = db.Column(db.Float)
#     decimalLongitude = db.Column(db.Float)
#     family = db.Column(db.String(64))
#     county = db.Column(db.String(64))
#     scientificName = db.Column(db.String(64))
#     vernacularName = db.Column(db.String(64))

    # def __repr__(self):
    #     return '<Animal %r>' % (self.vernacularName)

# Start the database [Only need if table don't exist]
# with app.app_context():
#     db.create_all()

#################################################
# Web User Interface - Front End
#################################################
# note that UI routes return a html response
# you can add as many html pages as you need
# below is an example to get you started...




# Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     print(request.method)
#     print(request.form)
#     if request.method == "POST":
#         animal_class = request.form['animal_class']
#         print("animal_class:", animal_class, type(animal_class))
#         basisOfRecord = request.form['basisOfRecord']
#         print("basisOfRecord:", basisOfRecord, type(basisOfRecord))
#         sex = request.form['sex']
#         print("sex:", sex, type(sex))
#         stateConservation = request.form['stateConservation']
#         print("stateConservation:", stateConservation, type(stateConservation))
#         protectedInNSW = request.form['protectedInNSW']
#         print("protectedInNSW:", protectedInNSW, type(protectedInNSW))
#         eventDate = request.form['eventDate']
#         print("eventDate:", eventDate, type(eventDate))
#         decimalLatitude = float(request.form['decimalLatitude'])
#         print("decimalLatitude:", decimalLatitude, type(decimalLatitude))
#         decimalLongitude = float(request.form['decimalLongitude'])
#         print("decimalLongitude:", decimalLongitude, type(decimalLongitude))
#         family = request.form['family']
#         print("family:", family, type(family))
#         county = request.form['county']
#         print("county:", county, type(county))
#         scientificName = request.form['scientificName']
#         print("scientificName:", scientificName, type(scientificName))
#         vernacularName = request.form['vernacularName']
#         print("vernacularName:", vernacularName, type(vernacularName))
#         uuid = request.form['uuid']
#         print("uuid:", uuid, type(uuid))
#         animal = Bionet(animal_class=animal_class, basisOfRecord = basisOfRecord , sex=sex,\
#                            stateConservation=stateConservation,protectedInNSW=protectedInNSW ,\
#                            eventDate=eventDate, decimalLatitude=decimalLatitude, decimalLongitude=decimalLongitude, family=family, county=county,\
#                            scientificName=scientificName,vernacularName=vernacularName,uuid=uuid)
#         print("created animal in flask")
#         db.session.add(animal)
#         db.session.commit()
#         print("created animal in database from flask")
#         return redirect("/", code=302)

#     return render_template("form.html")

# #################################################
# # API - Back End
# #################################################
# # we will use '/api/..' for our api within flask application
# # note that api returns a JSON response
# # you can add as many API routes as you need
# # below is an example to get you started...

# @app.route("/api/bionet")
# def bionet():
#     records = db.session.query(Bionet.uuid,Bionet.animal_class, Bionet.basisOfRecord,Bionet.sex,\
#                                      Bionet.stateConservation,Bionet.protectedInNSW ,Bionet.eventDate,\
#                                      Bionet.decimalLatitude,Bionet.decimalLongitude,Bionet.family,\
#                                      Bionet.county,Bionet.scientificName,Bionet.vernacularName).all()
    
#     # records = db.session.query.all()
#     records_list = []
#     for record in records:
#         record_dict = {
#             "uuid": record.uuid,
#             "animal_class": record.animal_class,
#             "basisOfRecord": record.basisOfRecord,
#             "sex": record.sex,
#             "stateConservation": record.stateConservation,
#             "protectedInNSW": record.protectedInNSW,
#             # "eventDate": record.eventDate.strftime("%Y-%m-%d"),
#             "decimalLatitude": record.decimalLatitude,
#             "decimalLongitude": record.decimalLongitude,
#             "family": record.family,
#             "county": record.county,
#             "scientificName": record.scientificName,
#             "vernacularName": record.vernacularName,
#         }
#         records_list.append(record_dict)
#     return jsonify(records_list)


if __name__ == "__main__":
    app.run(debug=True)
    # run the flask app
    # app.run()
