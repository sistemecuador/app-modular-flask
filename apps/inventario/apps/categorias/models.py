import os

from flask import url_for

from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.constantes import UPLOAD_FOLDER
from config.db import db


class Categorias(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(70), nullable=False, unique=True)
    descripcion = db.Column(db.String(100), nullable=True, default='No hay descripción')
    image = db.Column(db.String(100), nullable=True, default='')
    activo = db.Column(db.Boolean, default=True)
    product = db.relationship('Productos', backref='product', lazy='joined')

    def __init__(self, nombre_categoria, descripcion,
                 activo=True):
        super(Categorias, self).__init__()
        self.nombre_categoria = nombre_categoria
        self.descripcion = descripcion
        self.activo = activo

    def get_url_image(self):
        if self.image != '':
            return url_for('inventario.uploads',
                           sub_directorio='categorias',
                           filename=self.image)
        else:
            return url_for('static', filename='img/empty.png')

    def get_path_file(self):
        path_categorias = os.path.join(UPLOAD_FOLDER, 'categorias')
        path = os.path.join(path_categorias, self.image)
        if self.image != '':
            if os.path.exists(path):
                return path
        return None

    def remove_file(self, path):
        if path is not None:
            if os.path.exists(path):
                os.remove(path)

    @classmethod
    def crear_directorio(self, folder='categorias', filename=''):
        path = os.path.join(UPLOAD_FOLDER, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        if filename != '':
            path = os.path.join(path, filename)
        return path

    @classmethod
    def get_query_all(cls):
        lista = []
        for item in cls.get_all():
            tupla = (item.id, item.nombre_categoria)
            lista.append(tupla)
        return lista
