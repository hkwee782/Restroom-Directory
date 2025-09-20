from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/response")
def response():
    return render_template("response.html")

