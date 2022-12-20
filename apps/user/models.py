# import datetime
from sqlalchemy.orm import declared_attr

from base.auth.models import BaseUserModelMixin
from base.contrib.models import BaseModelMixin
from config.db import db

class User(BaseUserModelMixin, db.Model):
    __tablename__ = 'Users'
    image = db.Column(db.String(300), nullable=True)

    def __init__(self, image='', **kwargs):
        super(User, self).__init__(**kwargs)
        self.image = image
        self.password = self.set_password(kwargs.get("password"))

    def __repr__(self):
        return f'id: {self.id}-username: {self.username}'
