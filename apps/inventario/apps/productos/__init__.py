from flask import Blueprint

products = Blueprint("productos", __name__, template_folder="templates", url_prefix='/productos')

from . import routes
