from flask import Blueprint

app_user = Blueprint('user', __name__, template_folder='templates')

from . import routes
