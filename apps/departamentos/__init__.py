from flask import Blueprint

departamentos = Blueprint("departamentos", __name__, template_folder="templates", url_prefix='/departamentos')

from . import routes
