class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Usuario {} {}>'.format(self.username, self.email)



@app.route("/users/create", methods=["GET"])
def createUser():
    args = request.args
    username = args.get("username")
    email = args.get("email")
    password = args.get("password")

    if username == None or email == None or password == None:
        return "Missing parameters username, email, or password"
    
    passwordLength = len(password)
    hasNumber = False
    hasLetter = False
    for letter in password:
        if letter.isdigit():
            hasNumber = True
            break
    for letter in password:
        if letter.isalpha():
            hasLetter = True
            break
    
    if passwordLength < 8 or (not hasNumber) or (not hasLetter):
        return "invalid password, requires length 8, a number and a letter"
    
    try:
        newUser = Usuario(username=username, email=email, password=password)
        db.session.add(newUser)
        db.session.commit()
    except Exception as err:
        return "username already exists or email already exists"
    return "User added"

@app.route("/users/update/<username>", methods=["GET"])
def updateUser(username):
    oldUser = Usuario.query.filter(Usuario.username == username).first()

    if oldUser == None:
        return "No user with that username"

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
        pass
    
    oldUser.username = newUsername
    oldUser.password = newPassword
    oldUser.email = newEmail

    try:
        db.session.commit()
    except Exception as err:
        return "Invalid new parameters"
    return "User updated"

@app.route("/users/delete/<username>")
def deleteUser(username):
    user = Usuario.query.filter(Usuario.username == username).first()

    if user == None:
        return "No user with that username"
    
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as err:
        return "Error during delete"
    return "User deleted"