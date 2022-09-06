import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #coger nuestras variables de entorno (en .flaskenv) el URL de conexion para la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False