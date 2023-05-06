import pymongo
import os
# Connect to the MongoDB server
client = pymongo.MongoClient()

# Get the Yelp database
db = client.yelp

# Get the reviews collection
reviews = db.reviews

# Create a new database
yelp_reviews = client.yelp_reviews

# Create a new collection in the new database
review_data = yelp_reviews.review_data

# Create an index on the "stars" field
reviews.create_index("stars")

# Define a list of star values in descending order
star_values = [5, 4, 3, 2, 1]

# Define a counter to keep track of how many documents we've inserted
count = 0

# Loop through the star values
for star in star_values:
    # Find the first 20,000 documents where stars = star and select only the "stars" and "text" fields
    cursor = reviews.find({"stars": star}, {"stars": 1, "text": 1}).limit(20000)
    
    # Loop through the cursor and insert each document into the new collection
    for document in cursor:
        review_data.insert_one(document)
        count += 1
        
        # Break out of the loop if we've inserted 100,000 documents
        if count == 100000:
            break
            
    # Break out of the loop if we've inserted 100,000 documents
    if count == 100000:
        break

# Create a new directory called "instance" in the parent directory
instance_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "instance"))
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Export the "reviews" collection to a JSON file in the "instance" directory
export_file = os.path.join(instance_dir, "reviews.json")
with open(export_file, "w", encoding="utf-8") as f:
    cursor = review_data.find()
    for document in cursor:
        f.write(str(document) + "\n")