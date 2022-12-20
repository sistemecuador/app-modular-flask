import os.path

from flask import Blueprint

from config.constantes import BASE_DIR_P
print(BASE_DIR_P)
prestamos = Blueprint("prestamos", __name__, template_folder="templates", url_prefix='/prestamos',
                      static_folder='static')

from . import routes
