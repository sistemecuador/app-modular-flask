
from flask import Blueprint

inventario = Blueprint("inventario", __name__, template_folder="templates", url_prefix='/inventario')

from . import routes
