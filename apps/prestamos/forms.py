from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

from apps.departamentos.models import Departamentos


class FormBuscarProducto(FlaskForm):
    action = wtforms.HiddenField(default='buscar_productos')
    codigo_producto = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                                          render_kw={'class': 'form-control',
                                                     'placeholder': 'Ingrese el codigo de barra', 'autofocus': True,
                                                     'autocomplete': 'of'})

    categorias = wtforms.SelectField(choices=[(0, 'Categorias'), (1, 'productso')], coerce=int, default=[0],
                                     render_kw={'class': 'form-control selectpicker',
                                                'placeholder': 'Ingrese el codigo del producto',
                                                'data-live-search=True': True})


class ResponsableForm(FlaskForm):
    action = wtforms.HiddenField(default='buscar_responsable', render_kw={'class': 'action_tt'})
    identificador = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese el identificador del responsable'})


class TicketForm(FlaskForm):
    action = wtforms.HiddenField(default='generar_tt', render_kw={'class': 'action_tt'})
    dni = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                              render_kw={'class': 'form-control',
                                         'placeholder': 'Dni de la persona', 'readonly': True})
    nombres = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                                  render_kw={'class': 'form-control',
                                             'placeholder': 'Nombres completos', 'readonly': True})
    contacto = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                                   render_kw={'class': 'form-control',
                                              'placeholder': 'Contacto del responsable'})
    correo = wtforms.StringField(validators=[DataRequired(message="Este dato es requerido")],
                                 render_kw={'class': 'form-control',
                                            'placeholder': 'Correo electronico'})

    departamento = wtforms.SelectField(choices=[(0, 'Sin Asignar')], coerce=int, validate_choice=False,
                                       render_kw={'class': 'form-control',
                                                  'placeholder': 'Departamento de la empresa'})

    total_p = wtforms.IntegerField(default=0,
                                   render_kw={'class': 'form-control', 'readonly': True})
    observacion = wtforms.TextAreaField(validators=[DataRequired(message="Este dato es requerido")],
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese una observacion'})

    def set_departamentos_choice(self, lista):
        self.departamento.choices = self.departamento.choices + lista
