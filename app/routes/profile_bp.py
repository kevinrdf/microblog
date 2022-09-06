from flask import Blueprint
from app.controllers.ProfileController import profile, update

profile_bp = Blueprint('profile_bp', __name__)

profile_bp.route("/", methods=["GET"]) (profile)
profile_bp.route("/update", methods=["GET", "POST"]) (update)