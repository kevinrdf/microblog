from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Review {} {}>'.format(self.rating, self.description)


class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(8), index=True, unique=True)
    nombre = db.Column(db.String(20), index=True, unique=True)
    apellido = db.Column(db.String(20))

    def __repr__(self):
        return '<Estudiante {} {}>'.format(self.nombre, self.apellido)