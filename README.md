# AutoRator
Very often people are asked to give star reviews and/or comments on goods and services they have received. However, the existing rating experience in the market is not great:
1. Many users do not give star ratings that match the sentiment in their comments. This issue can be found in Google reviews, for example.
2. Many users give only star ratings but no comments. This does not help the service providers know where they are doing well and where they need to improve.

Here comes AutoRator, a machine learning-based rater that analyses the sentiment of a comment and categorises it as a positive, neutral or negative comment. In this way, rather than letting the user rate whether their experience is positive, negative or neutral, the user needs to write a comment and AutoRator automatically rates whether it is positive, neutral or negative.

### Content
AutoRator comes in the form of a webpage and focuses only on restaurant reviews. The webpage has a welcome page with an "open popup" button. Once the popup button is clicked, a popup page appears and there are options to select the restaurant needed 

### Development
There are several stages to developing AutoRator:
1. Retrieved all available comments and corresponding star ratings from the Yelp database and loaded them into MongoDB.
2. In MongoDB, filtered the dataset for restaurant reviews only, removed null and uncessary data and reduced the dataset to 888000 reviews.
3. Loaded the 888000 reviews from MongoDB into CSV files.
4. Set up, trained and tested several machine learning models with a subset of the data.
5. Assessed the accuracy scores for each model and they were lower than 0.7.
6. Determined the problem and optimised each model until we got models with accuracy scores greater than 0.75.
7. Selected the best model.
8. Set up the flask API to run the webpage.
9. Downloaded and modified a bootscrap template and then designed the webpage on that basis.
10. Developed the Emolex calculator and designed a graph that presents Emolex data for the comments extracted from Google reviews for a user-selected restaurant.
11. Produced a word cloud graphic that is based on the comments extracted from Google reviews for a user-selected restaurant.

### Data sources
1. Yelp Reviews
2. Google Reviews
3. Emolex

### Model optimisation, evaluation and selection
Several different models were used:
1. Random Forest
2. Keras Tokeniser
3. Linear Support Vector
4. Linear Regression
5. Naive Bayes Multinomial

After optimisation and evaluation of each model, we selected the linear regression model as the best machine learning model in this case, with an accuracy score of 0.76 and more balanced, well-rounded precisiona and recall scores for each cetegory of "positive", "neutral", "negative".

![Screenshot 2023-05-15 at 7 57 09 pm](https://github.com/davidj00/automatic-star-review/assets/115685811/bf7d0902-f1af-4ce5-8386-e5baa72d3f47)

### Instructions to run the programme
1. Activate your virtual environment
2. Pip install ?? module
3. In Git Bash, cd to the directory in which run.sh file is located on your local computer
4. Enter "chome a+x run.sh" (if running the flask for the first time) and then "./run.sh" to run the flask
