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
    return render_template("index.html")

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
    plt.tight_layout()
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


if __name__ == "__main__":
    app.run(debug=True)