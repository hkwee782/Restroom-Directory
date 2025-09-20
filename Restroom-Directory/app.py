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

if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
    app.run(debug = True, port=5000)


# Databases
class Building(db.Model):
    buildingID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.Double, nullable=False)
    lon = db.Column(db.Double, nullable=False)


class Bathroom(db.Model):
    buildingID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    floor = db.Column(db.Integer, primary_key= True, nullable=False)
    ReviewID = db.Column(db.Integer, foreign_key = True, nullable=False)

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True, foreign_key=True, nullable=False)
    wheelchair = db.Column(db.Boolean, nullable=True)
    menstrual = db.Column(db.Boolean, nullable=True)
    cleanliness = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(140), nullable=True) # only 140 characters

