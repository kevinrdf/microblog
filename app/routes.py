from app import app
from datetime import datetime
import re
from flask import render_template, request
from app.models import User, Review, Estudiante
from app import db
import requests
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'usuario'}
    return render_template('index.html', title='Home', user=user)
@app.route('/indexdinamico', methods=['GET'])
def indexDinamico():
    args = request.args
    title = args.get("title")
    username = args.get("username")
    user = {'username': username}
    return render_template('index.html', title=title, user=user)
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
    try:
        args = request.args
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")

        if (username == None):
            return "Falta parametro username"
        elif (password == None):
            return "Falta parametro password"
        elif (email == None):
            return "Falta parametro email"
        
        if (not verifyPassword(password)):
            return "Contrasena invalida"
        #returnString = "Username: " + username + " Password: " + password + "Email: " + email
        newUser = User(username=username, password=password, email=email)
        db.session.add(newUser)
        db.session.commit()
    except Exception as error:
        print("Invalid user", error)
        return "Invalid user"       
    return "User added"
@app.route("/addNumbers", methods=["GET"])
def add():
    args = request.args
    try:
        val1 = int(args.get("val1"))
    except Exception as error:
        print(error)
        return "val1 no es un numero"
    try:
        val2 = int(args.get("val2"))
    except Exception as error:
        print(error)
        return "val2 no es un numero"
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
    if rating > 5 or rating < 0:
        return "Ingrese un rating entre 0 y 5"
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
@app.route("/reviews/<id>/")
def getReview(id,pid):
    print(pid)
    review = Review.query.filter(Review.id == id).first()
    print(review)
    if review == None:
        return "No existe"
    return "Rating: " + str(review.rating) + "/5. Description: " + review.description
@app.route('/consolidarPaises')
def consolidarPaises():
    estudiantes = Estudiante.query.all()
    paises = {}

    # invoca el servicio web 
    # se recibe en un diccionario
    for estudiante in estudiantes:
        name = estudiante.nombre
        url = "https://api.nationalize.io/?name=" + name
        result = requests.get(url).json()
        pais = result["country"][0]["country_id"]
        # print(pais)
        if pais in paises:
            paises[pais] += 1
        else:
            paises[pais] = 1
    
    return paises



##### Estudiantes ######
@app.route("/estudiantes")
def getEstudiantes():
    estudiantes = Estudiante.query.all()
    estudianteEstring = ""
    for estudiante in estudiantes:
        estudianteEstring += "Nombre: " + estudiante.nombre + " Apellido: " + estudiante.apellido + "<br>"
    return estudianteEstring
@app.route("/estudiantes/create", methods=["GET"])
def createEstudiante():
    args = request.args
    codigo = args.get("codigo")
    nombre = args.get("nombre")
    apellido = args.get("apellido")
    
    newEstudiante = Estudiante(codigo=codigo, nombre=nombre, apellido=apellido)

    db.session.add(newEstudiante)
    db.session.commit()
    return "Estudiante creado"


def verifyPassword(password):
    return len(password) >= 10