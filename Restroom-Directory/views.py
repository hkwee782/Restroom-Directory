from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
# from app import db  # Assuming db is defined in app.py

views = Blueprint("views", __name__)

