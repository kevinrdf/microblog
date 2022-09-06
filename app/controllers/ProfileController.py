from app import app
import re
from flask import render_template, request, redirect
from app import db
from app.models import User

def profile():
    user = request.args
    username = user.get("username")
    password = user.get("password")
    return render_template("profile.html", username=username, password=password)