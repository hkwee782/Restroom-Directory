from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)

# Databases
class Building(db.Model):
    __tablename__ = 'building'
    bID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    opening = db.Column(db.DateTime(timezone=True), nullable=True)
    closing = db.Column(db.DateTime(timezone=True), nullable=True)
    bathrooms = db.relationship('Bathroom', backref='building', lazy=True)
    pass

class Bathroom(db.Model):
    __tablename__ = 'bathroom'
    bID = db.Column(db.Integer, db.ForeignKey('building.bID'), primary_key=True, nullable=False)
    floor = db.Column(db.Integer, primary_key= True, nullable=False)
    brID = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='bathroom', lazy=True)
    pass

class Review(db.Model):
    __tablename__ = 'review'
    brID = db.Column(db.Integer, db.ForeignKey('bathroom.brID'), nullable=False)
    rID = db.Column(db.Integer, primary_key=True, nullable=False)
    wheelchair = db.Column(db.Boolean, nullable=True)
    menstrual = db.Column(db.Boolean, nullable=True)
    cleanliness = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(140), nullable=True) # only 140 characters
    pass


# functions to add data
def initialize_buildings():
    buildings_data = [(1, "Cathedral of Learning", 40.44424, -79.95283),
                    (2, "Wesley W. Posvar Hall", 40.4416,-79.9538),
                    (3, "Michael L. Benedum Hall", 40.4436, -79.9587),
                    (4, "David Lawrence Hall", 40.4423869, -79.9549878)]

    for bID, name, lat, lon in buildings_data:
        if not db.session.get(Building, bID):
            db.session.add(Building(
                bID = bID,
                name = name,
                lat = lat,
                lon = lon
            ))
    db.session.commit()

def initialize_bathrooms():
    bathrooms_data = [(1, -1, 1),
                    (1, 2, 2),
                    (1, 32, 3),
                    (1, 20, 4),
                    (2, 5, 5),
                    (2, 1, 6),
                    (3, 8, 7),
                    (4, 2, 8),]

    for bID, floor, brID in bathrooms_data:
        if not Bathroom.query.filter_by(bID=bID, floor=floor).first():
            db.session.add(Bathroom(
                bID = bID,
                floor = floor,
                brID = brID
            ))
    db.session.commit()

def initialize_reviews():
    review_data = [(1, 1, True, False, 3, None),
                    (2, 2, False, False, 1, None),
                    (3, 3, True, True, 5, None),
                    (4, 4, False, True, 2, None)]

    for brID, rID, wheelchair, menstrual, clean, review in review_data:
        if not db.session.get(Review, rID):
            db.session.add(Review(
                brID = brID,
                rID = rID,
                wheelchair = wheelchair,
                menstrual = menstrual,
                cleanliness = clean,
                review = review
            ))
    db.session.commit()

def add_building(bID, name, lat, lon):
    if not db.session.get(Building, bID):
            db.session.add(Building(
                bID = bID,
                name = name,
                lat = lat,
                lon = lon
            ))
    db.session.commit()

def add_bathroom(bID, floor, rID):
    if not (db.session.get(Bathroom, bID) or db.session.get(Bathroom, floor)):
        db.session.add(Bathroom(
            bID = bID,
            floor = floor,
            brID = rID
        ))
    db.session.commit()

def add_review(brID, rID, wheelchair, menstrual, clean, review):
    if not db.session.get(Review, rID):
        db.session.add(Review(
            brID = brID,
            rID=rID,
            wheelchair = wheelchair,
            menstrual = menstrual,
            clean = clean,
            review = review
        ))
    db.session.commit()


# from views import views
# app.register_blueprint(views) # url_prefix="/views"

@app.route("/")
def home():
    buildings = Building.query.all()

    # Convert SQLAlchemy objects to dicts
    buildings_data = [
        {"id": b.bID, "name": b.name, "lat": b.lat, "lon": b.lon}
        for b in buildings
    ]
    avg_clean_data = db.session.query(
        Building.name, Bathroom.floor, func.avg(Review.cleanliness).label('avg_clean')
    ).join(
        Bathroom, Building.bID == Bathroom.bID
    ).join(
        Review, Bathroom.brID == Review.brID
    ).group_by(Building.name).all()

    return render_template("index.html", buildings=buildings, buildings_data=buildings_data, avg_clean=avg_clean_data)


@app.route("/response", methods=['GET', 'POST'])
def response():
    name = request.args.get('name', type=str)
    floor = request.args.get('floor', type=int)

    result = db.session.query(
        Building, Bathroom, Review, func.avg(Review.cleanliness).label('avg_clean')
    ).join(
        Bathroom, Building.bID == Bathroom.bID
    ).join(
        Review, Bathroom.brID == Review.brID
    ).filter(
        Building.name == name,
        Bathroom.floor == floor
    ).first()

    if result:
        building, bathroom, review, avg_clean = result
        # Pass the variables to the template
        return render_template(
            "response.html",
            name=building.name,
            floor=bathroom.floor,
            wheelchair=review.wheelchair,
            avg_clean=int(avg_clean),
            menstrual=review.menstrual,
            baby_station=False, # Assuming no baby station for now
            braille_signage=False # Assuming no braille signage for now
        )
    return render_template("response.html", name = name, floor = floor)

@app.route("/buildings", methods=['GET', 'POST'])
def buildings():
    buildings = Building.query.all()
    bathrooms = Bathroom.query.all()
    reviews = Review.query.all()
    return render_template("buildings.html", buildings=buildings, bathrooms=bathrooms, reviews=reviews)

if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
        initialize_buildings()
        initialize_bathrooms()
        initialize_reviews()
    app.run(debug = True, port=5000)

