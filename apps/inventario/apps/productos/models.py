import datetime
import os
from decimal import Decimal

from flask import url_for
from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper, ColumnProperty
from apps.inventario.apps.categorias.models import Categorias
from apps.inventario.apps.estados.models import EstadosProductos
from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.constantes import UPLOAD_FOLDER
from config.db import db


class UnidadDeMedida(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'unidad_de_medida'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
    nombre_unidad = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    productos = db.relationship(
        'Productos',
        backref='product_medida',
        lazy='dynamic'
    )

    def __init__(self, codigo, nombre_unidad, activo):
        self.codigo = codigo
        self.nombre_unidad = nombre_unidad
        self.activo = activo

    @classmethod
    def get_query_all(cls):
        lista = []
        for item in cls.get_all():
            tupla = (item.id, item.nombre_unidad)
            lista.append(tupla)
        return lista


class Productos(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.Date, index=True, default=None)
    name_producto = db.Column(db.String(70), nullable=False)
    marca = db.Column(db.String(50), nullable=True)
    codigo_producto = db.Column(db.String(100), nullable=True, unique=True)
    serie_producto = db.Column(db.String(100), nullable=True)
    modelo_producto = db.Column(db.String(100), nullable=True)
    descripcion = db.Column(db.String(70), nullable=True, default='No hay descripción')
    precio = db.Column(db.Numeric(10, 2), default=0.0)
    activo = db.Column(db.Boolean, default=True)
    estados_id = db.Column(db.Integer,
                           db.ForeignKey(EstadosProductos.id, ondelete='SET NULL'),
                           nullable=True)
    image = db.Column(db.String(100), nullable=True, default='')
    codigo_de_barra = db.Column(db.String(30), nullable=True, unique=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey(Categorias.id, ondelete='CASCADE'), nullable=False)
    medida_id = db.Column(db.Integer, db.ForeignKey(UnidadDeMedida.id, ondelete='SET NULL'), nullable=True)
    productos_salida = db.relationship('TicketsSalida', secondary='tickets_salida_productos',
                                       back_populates='tt_productos')
    productos_cierre = db.relationship('TicketsCerrados', secondary='tickets_cierre_productos',
                                       back_populates='tt_productos')

    def __init__(self, fecha_ingreso, marca, name_producto, descripcion, codigo_producto, serie_producto,
                 modelo_producto, precio, estados_id, categoria_id, medida_id=None, activo=True, **kwargs):
        self.marca = marca
        self.fecha_ingreso = fecha_ingreso
        self.name_producto = name_producto
        self.descripcion = descripcion
        self.codigo_producto = codigo_producto
        self.serie_producto = serie_producto
        self.modelo_producto = modelo_producto
        self.precio = precio
        self.estados_id = estados_id
        self.categoria_id = categoria_id
        self.medida_id = medida_id
        self.activo = activo
        self.kwargs = kwargs

    def set_obj(self, fecha_ingreso, marca, name_producto, descripcion, codigo_producto,
                serie_producto, modelo_producto, precio, estados_id, categoria_id, medida_id, activo, **kwargs):
        self.marca = marca
        self.fecha_ingreso = fecha_ingreso
        self.name_producto = name_producto
        self.descripcion = descripcion
        self.codigo_producto = codigo_producto
        self.serie_producto = serie_producto
        self.modelo_producto = modelo_producto
        self.precio = precio
        self.estados_id = estados_id
        self.categoria_id = categoria_id
        self.medida_id = medida_id
        self.activo = activo
        self.kwargs = kwargs
        return self

    def get_path_file(self):
        path_categorias = os.path.join(UPLOAD_FOLDER, 'productos')
        path = os.path.join(path_categorias, self.image)
        if self.image != '':
            if os.path.exists(path):
                return path
        print(path_categorias)
        print(path)
        return None

    @classmethod
    def remove_file(cls, path):
        if path is not None:
            if os.path.exists(path):
                os.remove(path)

    @classmethod
    def crear_directorio(self, folder='productos', filename=''):
        path = os.path.join(UPLOAD_FOLDER, folder)
        if not os.path.exists(path):
            os.mkdir(path)
        if filename != '':
            path = os.path.join(path, filename)
        return path

    @classmethod
    def get_list_all(cls, pk=None):
        lista = []
        for item in cls.get_all():
            if pk is not None:
                cls.query.filter_by(id=pk)
                for i in cls.get_all():
                    tupla = (i.id, i.name_producto)
                    lista.append(tupla)
            tupla = (item.id, item.name_producto)
            lista.append(tupla)
        return lista

    def generate_unix_time(self):
        id = str(self.id)
        ms = self.date_create
        utc_time = str(datetime.datetime.timestamp(ms) * 1000)
        utc_time = utc_time.split('.')[0]
        longitud = len(utc_time)
        numero = str(id)
        new_utc_time = utc_time[0:longitud - len(numero)] + numero
        self.codigo_de_barra = new_utc_time

    def get_url_image(self):
        if self.image != '':
            return url_for('inventario.uploads',
                           sub_directorio='productos',
                           filename=self.image)
        else:
            return url_for('static', filename='img/empty.png')

    def as_dict(self, exclude=[]):
        data = super(Productos, self).as_dict()
        data['image'] = self.get_url_image()
        print(data)
        return data
