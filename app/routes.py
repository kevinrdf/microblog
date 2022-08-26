from app import app
from datetime import datetime
import re
from flask import render_template, request
from app.models import User, Review
from app import db
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jose'}
    return render_template('index.html', title='Home', user=user)
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
@app.route("/add/user", methods=['GET'])
def addUser():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    email = args.get("email")
    #returnString = "Username: " + username + " Password: " + password + "Email: " + email
    newUser = User(username=username, password=password, email=email)
    db.session.add(newUser)
    db.session.commit()
    return "User added"
@app.route("/addNumbers", methods=["GET"])
def add():
    args = request.args
    val1 = int(args.get("val1"))
    val2 = int(args.get("val2"))
    return str(val1+val2)
@app.route("/users")
def getAllUsers():
    users = User.query.all()
    print(users)
    userStrings = ""
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"
    return userStrings
@app.route("/reviews/add", methods=["GET"])
def addReview():
    args = request.args
    rating = args.get("rating")
    description = args.get("description")
    newReview = Review(rating=rating, description=description)
    db.session.add(newReview)
    db.session.commit()
    return "Review added"
@app.route("/reviews")
def getReviews():
    reviews = Review.query.all()
    print(reviews)
    reviewString = ""
    for review in reviews:
        reviewString += "Rating: " + str(review.rating) + "/5. Description: " + review.description + "<br>"
    return reviewString
@app.route('/consolidarPaises')
def consolidarPaises():
    names = ["Pedro", "Jose", "Juan","Miguel","John","Paul","Sabrina","Katherina"]
    paises = {}

    # invoca el servicio web 
    # se recibe en un diccionario
    for name in names:
        url = "https://api.nationalize.io/?name=" + name
        result = requests.get(url).json()
        pais = result["country"][0]["country_id"]
        # print(pais)
        if pais in paises:
            paises[pais] += 1
        else:
            paises[pais] = 1
    
    return paises