from flask import Blueprint

bp = Blueprint('intellilearn', __name__)

from app.intellilearn import routes