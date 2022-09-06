from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

#inicializar la aplicacion app con la configuracion Config y la base de datos db
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#importar las rutas y modelos por si queremos usarlos
from app import routes, models

#podemos crear las tablas aqui si no queremos hacerlo manualmente
#db.create_all()