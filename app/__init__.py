from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

#inicializar la aplicacion app con la configuracion Config y la base de datos db
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#importar las rutas y modelos por si queremos usarlos
from app import models, topRoutes

from app.routes.login_bp import login_bp
from app.routes.profile_bp import profile_bp

app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(profile_bp, url_prefix="/profile")
#podemos crear las tablas aqui si no queremos hacerlo manualmente
#db.create_all()