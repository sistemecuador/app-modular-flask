from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.db import db


class Personal(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'personal'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    identificador = db.Column(db.String(30), nullable=False, unique=True)
    contacto = db.Column(db.String(30), nullable=True)
    correo = db.Column(db.String(100), nullable=False)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamentos.id', ondelete='SET NULL'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    personal_tt_salida = db.relationship('TicketsSalida', backref='personal_tickets_salida', lazy='dynamic')

    def __init__(self, nombre_completo, identificador, contacto, correo, id_departamento, activo):
        self.nombre_completo = nombre_completo
        self.identificador = identificador
        self.contacto = contacto
        self.correo = correo
        self.id_departamento = id_departamento
        self.activo = activo

    @classmethod
    def get_list_all(cls, pk=None):
        lista = []
        for item in cls.get_all():
            if pk is not None:
                cls.query.filter_by(id=pk)
                for i in cls.get_all():
                    tupla = (int(i.id), i.nombre_completo)
                    lista.append(tupla)
            tupla = (int(item.id), item.nombre_completo)
            lista.append(tupla)
        return lista
