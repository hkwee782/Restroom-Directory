from flask import Blueprint

views = Blueprint(__name__, "views")

@views.route("/")
def home_page():
    return "home page"