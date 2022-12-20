from base.contrib.models import BaseModelMixin, RelationShipAudit
from config.db import db
from flask_login import current_user


class EstadosProductos(db.Model, BaseModelMixin, RelationShipAudit):
    __tablename__ = 'estados_productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(70), nullable=False, unique=True)
    activo = db.Column(db.Boolean, default=True)
    product = db.relationship('Productos', backref='estados_productos', lazy='dynamic')

    def __repr__(self):
        return f'{str(self.id)}', self.nombre_estado

    def __init__(self, nombre_estado, activo=True):
        super(EstadosProductos, self).__init__()
        self.nombre_estado = nombre_estado
        self.activo = activo

    @classmethod
    def get_query_all(cls, pk=None):
        lista = []

        for item in cls.get_all():
            if pk is not None:
                cls.query.filter_by(id=pk)
                for i in cls.get_all():
                    tupla = (i.id, i.nombre_estado)
                    lista.append(tupla)
            tupla = (item.id, item.nombre_estado)
            lista.append(tupla)

        return lista
