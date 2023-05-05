# import necessary libraries
# import os
from flask import (
    Flask,
    render_template)
    # jsonify,
    # request,
    # redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

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

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("test.html")


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
