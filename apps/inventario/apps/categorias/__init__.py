from flask import Blueprint

categorias = Blueprint("categorias", __name__, template_folder="templates", url_prefix='/categorias')

from . import routes
