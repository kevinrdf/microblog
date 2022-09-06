#importamos nuestra app
from app import app
#para manipular fechas
from datetime import datetime
#para manipular regular expressions
import re
#importamos render_template y request para usarlos en nuestras rutas
from flask import render_template, request
#importamos los modelos que vamos a usar en nuestras rutas
from app.models import User, Review, Estudiante, Usuario
#importamos la db para mandar solicitudes
from app import db
#estos modulos son utiles para manejar APIs
import requests
import json

#varias rutas pueden estar definidas por la misma funcion
@app.route('/')
@app.route('/index')
#la funcion define el comportamiento del servidor al ser solicitado una ruta
def index():
    #creamos un diccionario
    user = {'username': 'usuario'}
    #la funcion render_template reemplaza los parametros pasados en
    #el archivo del primer parametro y devuelve el html correspondiente al cliente
    return render_template('index.html', title='Home', user=user, elemento1="codigo", elemento2="HTML")
#por defecto todas las rutas usan GET pero podemos especificarlo usando el parametro
#methods, especialmente si vamos a aceptar mas de un metodo para la misma ruta
@app.route('/indexdinamico', methods=['GET'])
def indexDinamico():
    #podemos usar el modulo request de Flask para obtener parametros del URL
    #en este caso esperamos que el usuario mande los parametros title y username
    #e.j. localhost:5000/indexdinamico?title=titulo&username=jpazos
    args = request.args
    title = args.get("title")
    username = args.get("username")
    user = {'username': username}
    return render_template('index.html', title=title, user=user)
#los <> definen un path parameter, cualquier valor que el usuario pase despues de
#"/hello/" sera el input de la funcion hello_there
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
    #usamos el try para poder recuperarnos de algun errro
    try:
        #esta ruta espera tres parametros
        args = request.args
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        #el usuario podria no mandar los parametros, hay que verificar que sean validos
        if (username == None):
            return "Falta parametro username"
        elif (password == None):
            return "Falta parametro password"
        elif (email == None):
            return "Falta parametro email"
        
        if (not verifyPassword(password)):
            return "Contrasena invalida"
        #creamos un nuevo usuario de clase User 
        newUser = User(username=username, password=password, email=email)
        #agregamos el usuario a la sesion actual de la db
        db.session.add(newUser)
        #mandamos los cambios para que persistan en la db
        db.session.commit()
    #en caso ocurra un error podemos recuperarnos sin romper el flujo del programa    
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
    #podemos pedir la informacion de varias filas de la tabla
    #al mismo tiempo usando 'query.all()', esto devuelve una lista
    users = User.query.all()
    print(users)
    userStrings = ""
    #podemos iterar por el resultado como cualquier lista
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"
    return userStrings
@app.route("/reviews/add", methods=["GET"])
def addReview():
    args = request.args
    rating = args.get("rating")
    #podemos realizar alguna verificacion en los datos si no queremos
    #hacerlo en la base de datos (aunque seria mejor hacerlo alla)
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
def getReview(id):
    #query nos permite filtrar datos basado en ciertas condiciones
    #aqui estamos filtrando la fila que tenga el mismo id que se paso en el URL
    #la funcion first() coge el primer valor del resultado
    review = Review.query.filter(Review.id == id).first()
    print(review)
    #siempre verificar si tenemos un dato valido antes de acceder a sus propiedades
    if review == None:
        return "No existe"
    return "Rating: " + str(review.rating) + "/5. Description: " + review.description
#Esta ruta se comunica con un API externo, nationalize,
#que retorna un objeto JSON con probabilidades que el nombre
#dado venga de un pais especifico
#este es un ejemplo de un request
#https://api.nationalize.io/?name=jose
#y un ejemplo de la respuesta
# {
#   "name": "jose",
#   "country": [
#     {
#       "country_id": "VE",
#       "probability": 0.05786648552663837
#     },
#     {
#       "country_id": "ES",
#       "probability": 0.05710861497406078
#     },
#     {
#       "country_id": "SV",
#       "probability": 0.05705595515479477
#     }
#   ]
# }

@app.route('/consolidarPaises')
def consolidarPaises():
    estudiantes = Estudiante.query.all()
    paises = {}

    # invoca el servicio web 
    # se recibe en un diccionario
    for estudiante in estudiantes:
        name = estudiante.nombre
        #
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

###solucion de ejercicio en clase
@app.route("/users/create", methods=["GET"])
def createUser():
    args = request.args
    username = args.get("username")
    email = args.get("email")
    password = args.get("password")

    if username == None or email == None or password == None:
        return "Missing parameters: username, email or password"
    passwordLength = len(password)
    hasDigit = False
    hasLetter = False
    for letter in password:
        if letter.isdigit():
            hasDigit = True
            break
    for letter in password:
        if letter.isalpha():
            hasLetter = True
            break
    if passwordLength < 8 or (not hasDigit) or (not hasLetter):
        return "Invalid password, must have at least 8 characters, a digit and a letter"
    newUser = Usuario(username=username, email=email, password=password)
    db.session.add(newUser)
    try:
        db.session.commit()
    except Exception as err:
        return "Invalid user"
    return "User added"

@app.route('/users/update/<username>', methods=['GET'])
def updateUser(username):
    oldUser = Usuario.query.filter(Usuario.username == username).first()

    if oldUser == None:
        return "User not found"
    
    args = request.args
    newUsername = args.get("username")
    newEmail = args.get("email")
    newPassword = args.get("password")

    if newUsername == None:
        newUsername = oldUser.username
    if newEmail == None:
        newEmail = oldUser.email
    if newPassword == None:
        newPassword = oldUser.password
    else:
        #verificar contrasena
        #verificarContrasena(password)
        pass
    
    oldUser.username = newUsername
    oldUser.email = newEmail
    oldUser.password = newPassword

    try:
        db.session.commit()
    except Exception as err:
        return "Update paramaters are invalid"
    return "User updated"

@app.route('/users/delete/<username>')
def deleteUser(username):
    user = Usuario.query.filter(Usuario.username == username).first()

    if user == None:
        return "User not found"
    
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as err:
        return "Invalid user deletion"
    return "User deleted"

@app.route("/base")
def base():
    return render_template("base.html")

# @app.route("/login/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         return "login attempt for username " + username
#     return render_template("login.html")