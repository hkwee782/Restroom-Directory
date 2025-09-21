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
    __tablename__ = 'building'
    bID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    bathrooms = db.relationship('Bathroom', backref='building', lazy=True)

class Bathroom(db.Model):
    __tablename__ = 'bathroom'
    brID = db.Column(db.Integer, db.ForeignKey('building.bID'), primary_key=True, nullable=False)
    floor = db.Column(db.Integer, primary_key= True, nullable=False)
    rID = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='bathroom', lazy=True)

class Review(db.Model):
    __tablename__ = 'review'
    brID = db.Column(db.Integer, db.ForeignKey('bathroom.bID'), nullable=False)
    rID = db.Column(db.Integer, primary_key=True, nullable=False)
    wheelchair = db.Column(db.Boolean, nullable=True)
    menstrual = db.Column(db.Boolean, nullable=True)
    cleanliness = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(140), nullable=True) # only 140 characters

# functions to add data
def initialize_buildings():
    buildings_data = [(1, "Cathedral of Learning", 40.44424, -79.95283),
                    (2, "Wesley W. Posvar Hall", 40.4416,-79.9538),
                    (3, "Michael L. Benedum Hall", 40.4436, -79.9587),
                    (4, "David Lawrence Hall", 40.4423869, -79.9549878)]

    for bID, name, lat, lon in buildings_data:
        if not Building.query.get(bID):
            db.session.add(Building(
                bID = bID,
                name = name,
                lat = lat,
                lon = lon
            ))
    db.session.commit()

def add_building(bID, name, lat, lon):
    if not Building.query.get(bID):
            db.session.add(Building(
                bID = bID,
                name = name,
                lat = lat,
                lon = lon
            ))
    db.session.commit()

def add_bathroom(bID, floor, rID):
    if not Bathroom.query.get(bID):
        db.session.add(Bathroom(
            bID=bID,
            floor = floor,
            rID = rID
        ))
    db.session.commit()

def add_review(brID, rID, wheelchair, menstrual, clean, review):
    if not Review.query.get(rID):
        db.session.add(Review(
            brID = brID,
            rID=rID,
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