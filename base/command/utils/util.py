import os
import re

import click
from apps.user.models import User
from config.constantes import BASE_DIR_P
from utils.util import create_file
from app import app


class Decorator(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('Dentro del Decorador.')
        return self.func(*args, **kwargs)


class CommandBase:

    @staticmethod
    @app.cli.command("createapp")
    @click.argument("name")
    def create_apps(name):
        """
        Permite crear una aplicacion modularizada
        :param name: Nombre de el aplicacion
        :return: None
        """
        FILES = ['__init__.py', 'forms.py', 'models.py', 'models.py']
        FOLDER = ['templates', 'static']
        PACKAGE = name
        PATH = os.path.join(BASE_DIR_P, PACKAGE)
        if not os.path.exists(PATH):
            os.mkdir(PATH)
            for item in FOLDER:
                path_folder = os.path.join(PATH, item)
                os.mkdir(path_folder)
            for file in FILES:
                create_file(PATH, file, package=PACKAGE, blueprint=True)
        else:
            raise Exception(f"La aplicacion {name} ya existe")

    @staticmethod
    @app.cli.command("createsuperuser")
    @click.option('--username', prompt=True)
    @click.option('--password', prompt=True)
    @click.option('--email', prompt=True)
    def create_super_user(username, password, email):
        try:
            click.echo(f'{username}')
            click.echo(f'{password}')
            click.echo(f'{email}')
            user = User(username=username, password=password, email=email)
            if user.validate_email():
                user.save()
            else:
                raise Exception("Email no es valido")
        except Exception as e:
            print("Error", str(e))
