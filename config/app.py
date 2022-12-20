from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config.constantes import BASE_STATIC_ROOT, BASE_TEMPLATE_ROOT
from config.db import db
from config.settings import config


def page_not_found(e):
    return render_template('errors/400.html'), 404


def create_app():
    app = Flask(__name__, template_folder=BASE_TEMPLATE_ROOT, static_folder=BASE_STATIC_ROOT)
    app.config.from_object(config['development'])
    # csrf = CSRFProtect()
    # csrf.init_app(app)
    db.init_app(app)
    from apps.user import app_user
    app.register_blueprint(app_user)
    from apps.home import home
    app.register_blueprint(home)
    from apps.login import login
    app.register_blueprint(login)
    from apps.inventario.apps.productos import products
    app.register_blueprint(products)
    from apps.inventario.apps.categorias import categorias
    app.register_blueprint(categorias)
    from apps.inventario.apps.estados import estados
    app.register_blueprint(estados)
    from apps.inventario import inventario
    app.register_blueprint(inventario)
    from apps.tickets import tickets
    app.register_blueprint(tickets)
    from apps.personal import personal
    app.register_blueprint(personal)
    from apps.departamentos import departamentos
    app.register_blueprint(departamentos)
    from apps.prestamos import prestamos
    app.register_blueprint(prestamos)
    app.register_error_handler(404, page_not_found)
    return app
