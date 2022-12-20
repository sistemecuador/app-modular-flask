import calendar
import datetime
import time

from apps.personal.models import Personal
from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.db import db


class TicketsSalidaProductos(db.Model):
    __tablename__ = 'tickets_salida_productos'
    id = db.Column(db.Integer, primary_key=True)
    id_tickctes_salida = db.Column('id_tickctes_salida', db.Integer,
                                   db.ForeignKey('tickets_salida.id', ondelete='CASCADE'), nullable=False)
    id_productos = db.Column('id_productos', db.Integer, db.ForeignKey('productos.id', ondelete='CASCADE'),
                             nullable=False)


class TicketsSalida(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'tickets_salida'
    id = db.Column(db.Integer, primary_key=True)
    tt_salida = db.Column(db.String(30), nullable=True, unique=True)
    fecha_salida = db.Column(db.Date, default=datetime.date.today(), nullable=False)
    obs_salida = db.Column(db.String(100), nullable=False, default='N-A')
    estado_salida = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)
    id_personal = db.Column(db.Integer, db.ForeignKey(Personal.id, ondelete='CASCADE'), nullable=True)
    tickets_salida_cerrado = db.relationship('TicketsCerrados', backref='tickets_salida_cerrado', lazy='dynamic')
    tt_productos = db.relationship('Productos', secondary='tickets_salida_productos', back_populates='productos_salida')

    def __init__(self, fecha_salida, obs_salida, estado_salida, activo, id_personal):
        self.fecha_salida = fecha_salida
        self.obs_salida = obs_salida
        self.estado_salida = estado_salida
        self.activo = activo
        self.id_personal = id_personal

    def get_tt(self):
        return [(self.id, self.tt_salida)]

    def get_list_products(self):
        productos = self.tt_productos
        lista = []
        for item in productos:
            lista.append((item.id, item.name_producto))
        return lista

    @classmethod
    def get_list_all(cls):
        lista = []
        for item in cls.get_all():
            lista.append((item.id, item.tt_salida))
        return lista

    @classmethod
    def generate_unix(cls, id):
        id = str(id)
        ms = datetime.datetime.now()
        utc_time = str(datetime.datetime.timestamp(ms) * 1000)
        utc_time = utc_time.split('.')[0]
        longitud = len(utc_time)
        numero = str(id)
        new_utc_time = utc_time[0:longitud - len(numero)] + numero
        return new_utc_time

    def generate_unix_time(self):
        id = str(self.id)
        ms = self.date_create
        utc_time = str(datetime.datetime.timestamp(ms) * 1000)
        utc_time = utc_time.split('.')[0]
        longitud = len(utc_time)
        numero = str(id)
        new_utc_time = utc_time[0:longitud - len(numero)] + numero
        self.tt_salida = new_utc_time


class TicketsCierreProductos(db.Model):
    __tablename__ = 'tickets_cierre_productos'
    id = db.Column(db.Integer, primary_key=True)
    id_tickets_cierre = db.Column('id_tickets_cierre', db.Integer,
                                  db.ForeignKey('tickets_cerrados.id', ondelete='CASCADE'))
    id_productos = db.Column('id_productos', db.Integer, db.ForeignKey('productos.id', ondelete='CASCADE'))


class TicketsCerrados(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'tickets_cerrados'
    id = db.Column(db.Integer, primary_key=True)
    tt_cierre = db.Column(db.String(30), nullable=True, unique=True)
    fecha_cierre = db.Column(db.Date, default=datetime.date.today(), nullable=False)
    obs_cierre = db.Column(db.String(100), nullable=False, default='N-A')
    estado_cierre = db.Column(db.Boolean, default=False)
    id_tickets_salida = db.Column(db.Integer, db.ForeignKey(TicketsSalida.id, ondelete='CASCADE'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    tt_productos = db.relationship('Productos', secondary='tickets_cierre_productos', back_populates='productos_cierre')

    def __init__(self, fecha_cierre, obs_cierre, estado_cierre, activo, id_tickets_salida):
        self.fecha_cierre = fecha_cierre
        self.obs_cierre = obs_cierre
        self.estado_cierre = estado_cierre
        self.activo = activo
        self.id_tickets_salida = id_tickets_salida

    def get_tt(self):
        return [(self.id, self.tt_cierre)]

    def get_list_products(self):
        productos = self.tt_productos
        lista = []
        for item in productos:
            lista.append((item.id, item.name_producto))
        return lista

    @classmethod
    def get_list_all(cls):
        lista = []
        for item in cls.get_all():
            lista.append((item.id, item.tt_cierre))
        return lista

    @classmethod
    def generate_unix(cls, id):
        id = str(id)
        ms = datetime.datetime.now()
        utc_time = str(datetime.datetime.timestamp(ms) * 1000)
        utc_time = utc_time.split('.')[0]
        longitud = len(utc_time)
        numero = str(id)
        new_utc_time = utc_time[0:longitud - len(numero)] + numero
        return new_utc_time

    def generate_unix_time(self):
        print("se genero el codigo")
        id = str(self.id)
        ms = self.date_create
        utc_time = str(datetime.datetime.timestamp(ms) * 1000)
        utc_time = utc_time.split('.')[0]
        longitud = len(utc_time)
        numero = str(id)
        new_utc_time = utc_time[0:longitud - len(numero)] + numero
        self.tt_cierre = new_utc_time
