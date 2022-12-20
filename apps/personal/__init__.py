from flask import Blueprint

personal = Blueprint("personal", __name__, template_folder="templates", url_prefix='/personal')

from . import routes
