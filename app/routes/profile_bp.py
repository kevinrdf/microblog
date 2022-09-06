from flask import Blueprint
from app.controllers.ProfileController import profile

profile_bp = Blueprint('profile_bp', __name__)

profile_bp.route("/", methods=["GET"]) (profile)
#profile_bp.route("/register", methods=["GET", "POST"]) (register)