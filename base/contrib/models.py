import datetime
import sys
from decimal import Decimal

from sqlalchemy.orm import declared_attr, class_mapper, ColumnProperty
from config.db import db
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, UserMixin


class Apps:
    def __init__(self, apps=()):
        # installed_apps is set to None when creating the master registry
        # because it cannot be populated at that point. Other registries must
        # provide a list of installed apps and are populated immediately.
        if apps is None and hasattr(sys.modules[__name__], 'apps'):
            raise RuntimeError("You must supply an installed_apps argument.")


class AbstractUser:
    """
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    """

    # Python 3 implicitly set __hash__ to None if we override __eq__
    # We set it back to its default implementation
    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    # @property
    # def is_superuser(self):
    #     return False
    #
    # @property
    # def _is_superuser(self):
    #     return self.is_superuser
    #
    # @property
    # def is_admin(self):
    #     return False
    #
    # @property
    # def _is_admin(self):
    #     return self.is_admin

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, AbstractUser):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin:
    """
    This is the default object for representing an anonymous user.
    """

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return


class RelationShipAudit:

    @staticmethod
    def get_user_id():
        from apps.user.models import User
        return User.id

    @declared_attr
    def user_create(self):
        user_create = db.Column(db.Integer, db.ForeignKey(self.get_user_id(), ondelete='SET NULL'), nullable=True)
        return user_create

    @declared_attr
    def user_update(self):
        user_update = db.Column(db.Integer, db.ForeignKey(self.get_user_id(), ondelete='SET NULL'), nullable=True)
        return user_update

    @declared_attr
    def rl_user_create(self):
        rl_user_create = db.relationship(
            'User',
            backref=self.__name__ + '_create',
            # cascade='save-update, merge, delete',
            passive_deletes=True,
            # lazy='dynamic',
            foreign_keys=[self.user_create]
        )
        return rl_user_create

    @declared_attr
    def rl_user_update(self):
        rl_user_update = db.relationship(
            'User',
            backref=self.__name__ + '_update',
            # cascade='save-update, merge, delete',
            passive_deletes=True,
            # lazy='dynamic',
            foreign_keys=[self.user_update]
        )
        return rl_user_update


class BaseModelMixin:
    date_create = db.Column(db.DateTime, index=True, default=datetime.datetime.now())

    date_update = db.Column(db.DateTime, index=True, default=None)

    def save(self, commit=False, callback=None, **kwargs):
        try:
            self.check_audit()
            self.__change_date_update()
            if not commit:
                db.session.add(self)
            else:
                db.session.add(self)
            if callback:
                new_path, change_codigo, old_path = kwargs.get("new_path"), kwargs.get("change_codigo"), kwargs.get(
                    "old_path")
                print("Ejecutando callback")
                callback(new_path, change_codigo, old_path)
            if kwargs.get('list_objects'):
                for item in kwargs.get('list_objects'):
                    db.session.add(item)
        except IntegrityError as e:
            error = str(e.orig)
            db.session.rollback()
            raise Exception(error)
        except Exception as e:
            error = str(e)
            db.session.rollback()
            raise Exception(error)
        else:
            db.session.commit()
        return self

    def check_audit(self):
        if current_user != None:
            if current_user.is_authenticated:
                if hasattr(self, 'rl_user_create') and hasattr(self, 'rl_user_update'):
                    if self.date_create is None:
                        self.rl_user_create = current_user
                    else:
                        self.__change_date_update()
                        self.rl_user_update = current_user

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            error = str(e.orig)
            print("erro desde delete", str(error))
            raise Exception(error)
        except Exception as e:
            error = str(e)
            db.session.rollback()
            raise Exception(error)
        finally:
            db.session.rollback()

    def rollback(self):
        db.session.rollback()
        db.session.remove()

    def __change_date_update(self):
        if self.date_create is not None:
            self.date_update = datetime.datetime.now()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def as_dict(self, exclude=[]):
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                value = getattr(self, prop.key)
                if isinstance(value, datetime.date) and prop.key not in exclude:
                    if value is not None:
                        result[prop.key] = str(value.strftime('%Y-%m-%d'))
                    else:
                        result[prop.key] = '-'
                elif isinstance(value, datetime.datetime) and prop.key not in exclude:
                    if value is not None:
                        result[prop.key] = str(value.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        result[prop.key] = '-'
                elif isinstance(value, Decimal) and prop.key not in exclude:
                    if value is not None:
                        result[prop.key] = f'{Decimal(value).__str__()}'
                    else:
                        result[prop.key] = '-'
                else:
                    if prop.key not in exclude:
                        result[prop.key] = value
        return result
