from flask import Blueprint

bp = Blueprint('actiscore', __name__)

from app.actiscore import routes