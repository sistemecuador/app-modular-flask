import datetime

from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as vt

from apps.inventario.apps.productos.models import Productos


class Productos_item:

    @classmethod
    def get_list(cls):
        return [i[0] for i in Productos.get_list_all()]


class TicketsSalidaForm(FlaskForm):
    fecha_salida = wtforms.DateField(label='Fecha de salida', default=datetime.date.today(),
                                     validators=[vt.DataRequired()], render_kw={'class': 'form-control'})
    id_personal = wtforms.SelectField(label='Responsable', coerce=str, choices=[],
                                      render_kw={'class': 'form-control'})

    observacion_salida = wtforms.TextAreaField(label='Observacion', default='N-A',
                                               validators=[vt.DataRequired(), vt.Length(max=100)],
                                               render_kw={'class': 'form-control',
                                                          'placeholder': 'Ingrese una observacion'})
    tt_productos = wtforms.SelectMultipleField(label='Productos', coerce=int, validators=[vt.DataRequired()],
                                               choices=[],
                                               render_kw={'class': 'form-control'})

    activo = wtforms.BooleanField(default=True)
    estado_salida = wtforms.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super(TicketsSalidaForm, self).__init__(*args, **kwargs)
        self.list_productos = kwargs.get("list_productos", None)

    def set_productos_salida(self, lista):
        self.tt_productos.choices = self.tt_productos.choices + lista

    def set_id_personal(self, lista):
        self.id_personal.choices = self.id_personal.choices + lista


class TicketsCierreForm(FlaskForm):
    fecha_cierre = wtforms.DateField(label='Fecha de cierre', default=datetime.date.today(),
                                     validators=[vt.DataRequired()], render_kw={'class': 'form-control'})
    id_tickets_salida = wtforms.SelectField(label='Ticket Salida', coerce=str, choices=[],
                                            render_kw={'class': 'form-control'})
    obs_cierre = wtforms.TextAreaField(label='Observacion', default='N-A',
                                       validators=[vt.DataRequired(), vt.Length(max=100)],
                                       render_kw={'class': 'form-control',
                                                  'placeholder': 'Ingrese una observacion'})
    tt_productos = wtforms.SelectMultipleField(label='Productos entregados', coerce=int,
                                               choices=[],
                                               render_kw={'class': 'form-control'})

    tt_productos_devueltos = wtforms.SelectMultipleField(label='Productos devueltos', coerce=int,
                                                         choices=[],validate_choice=False,
                                                         render_kw={'class': 'form-control'})

    activo = wtforms.BooleanField(default=True)
    estado_cierre = wtforms.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(TicketsCierreForm, self).__init__(*args, **kwargs)
        # self.list_productos = kwargs.get("list_productos", None)
        # self.list_productos_devueltos = kwargs.get("list_productos_devueltos", None)

    def set_productos_entregados(self, lista):
        self.tt_productos.choices = self.tt_productos.choices + lista

    def set_productos_devueltos(self, lista):
        self.tt_productos_devueltos.choices = self.tt_productos_devueltos.choices + lista

    def set_id_ticket_salida(self, lista):
        self.id_tickets_salida.choices = self.id_tickets_salida.choices + lista
