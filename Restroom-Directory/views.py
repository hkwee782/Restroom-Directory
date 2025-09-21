from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
# import db  # Assuming db is defined in app.py

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/response")
def response():
    return render_template("response.html")

@views.route("/buildings")
def show_buildings():
    buildings = Building.query.all()
    return render_template("buildings.html", buildings=buildings)