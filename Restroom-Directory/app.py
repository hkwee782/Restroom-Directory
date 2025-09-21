from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from views import views

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)

app.register_blueprint(views) # url_prefix="/views"

# Databases
class Building(db.Model):
    buildingID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

class Bathroom(db.Model):
    bathroomID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    floor = db.Column(db.Integer, primary_key= True, nullable=False)
    ReviewID = db.Column(db.Integer, foreign_key = True, nullable=False)

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    wheelchair = db.Column(db.Boolean, nullable=True)
    menstrual = db.Column(db.Boolean, nullable=True)
    cleanliness = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(140), nullable=True) # only 140 characters

# functions to add data
def initialize_buildings():
    buildingID = [1,2,3,4]
    name = ["Cathedral of Learning",
                "Wesley W. Posvar Hall",
                "Michael L. Benedum Hall",
                "David Lawrence Hall"]

    lat = [40.44424, 40.4416, 40.4436, 40.4423869]
    lon = [-79.95283, -79.9538, -79.9587, -79.9549878]

    for i in range(4):
        if not buildingID.query.filter_by(buildingID=buildingID).first():
            db.session.add(Building(
                buildingID = buildingID[i],
                name = name[i],
                lat = lat[i],
                lon = lon[i]
            ))
    db.session.commit()

def add_building(id, name, lat, lon):
    if not Building.query.filter_by(buildingID=id).first():
            db.session.add(Building(
                buildingID = id,
                name = name,
                lat = lat,
                lon = lon
            ))
    db.session.commit()

def add_bathroom(bID, floor, rID):
    if not Bathroom.query.filter_by(buildingID=bID).first():
        db.session.add(Bathroom(
            buildingID=bID,
            floor = floor,
            reviewID = rID
        ))
    db.session.commit()

def add_review(rID, wheelchair, menstrual, clean, review):
    if not Review.query.filter_by(reviewID=rID).first():
        db.session.add(Review(
            reviewID=rID,
            wheelchair = wheelchair,
            menstrual = menstrual,
            clean = clean,
            review = review
        ))
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
    app.run(debug = True, port=5000)