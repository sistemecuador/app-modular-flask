from flask import Blueprint

tickets = Blueprint("tickets", __name__, template_folder="templates", url_prefix='/tickets')

from . import routes
