from flask import Blueprint

views = Blueprint("views")

@views.route("/")
def home_page():
    return "home page"