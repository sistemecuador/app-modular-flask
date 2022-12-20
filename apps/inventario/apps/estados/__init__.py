from flask import Blueprint

estados = Blueprint("estados", __name__, template_folder="templates",url_prefix='/estados')

from . import routes