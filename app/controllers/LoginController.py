from app import app
import re
from flask import render_template, request, redirect
from app import db
from app.models import User
import requests
import json
from cryptography.hazmat.primitives import hashes

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return "Missing form parameter username or password"
        try:
            user = User.query.filter(User.username == username).first()
            if user == None or password != user.password:
                return "Invalid user or password"
            email = user.email
            password = bytes(password, "utf-8")
            digest = hashes.Hash(hashes.SHA256())
            digest.update(password)
            hashedPassword = str(digest.finalize())
            return redirect("/profile?username="+username+"&password="+hashedPassword+"&email="+email)
        except Exception as err:
            print(err)
            return "Error while accesing user. Try again."
    return render_template("login.html")

def register():
    return "register"
