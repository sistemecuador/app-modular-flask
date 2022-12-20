from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.db import db


class Departamentos(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_departamento = db.Column(db.String(50), nullable=False, unique=True)
    observacion = db.Column(db.String(100), nullable=True, default='N-A')
    activo = db.Column(db.Boolean, default=True)
    personal = db.relationship('Personal', backref='departamentos_personal', lazy='dynamic')

    def __init__(self, nombre_departamento, observacion, activo):
        self.nombre_departamento = nombre_departamento
        self.observacion = observacion
        self.activo = activo

    @classmethod
    def get_list_all(cls, pk=None):
        lista = []
        for item in cls.get_all():
            if pk is not None:
                cls.query.filter_by(id=pk)
                for i in cls.get_all():
                    tupla = (i.id, i.nombre_departamento)
                    lista.append(tupla)
            tupla = (item.id, item.nombre_departamento)
            lista.append(tupla)
        return lista

    def get_list_departamento(self):
        lista = []
        tupla = (self.id, self.nombre_departamento)
        lista.append(tupla)
        return lista
