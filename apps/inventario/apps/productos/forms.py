import datetime

from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as vt
import wtforms.widgets as wg

from apps.inventario.apps.estados.models import EstadosProductos
from apps.inventario.apps.productos.models import Productos

#validators=[vt.DataRequired(message="Este dato es requerido")]

class ProductosForm(FlaskForm):
    fecha_ingreso = wtforms.DateField(label='Fecha de llegada', default=datetime.date.today(),
                                      validators=[vt.DataRequired(message="Este dato es requerido")],
                                      render_kw={'class': 'form-control',
                                                 'placeholder': 'Ingrese la fecha de llegada'})
    codigo_producto = wtforms.StringField(label='Ingrese el codigo del producto',
                                          render_kw={'class': 'form-control',
                                                     'placeholder': 'Ingrese el codigo del producto'})
    name_producto = wtforms.StringField(label='Nombre del producto',
                                        validators=[vt.DataRequired(message="Este dato es requerido")],
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese el nombre del producto'})
    marca = wtforms.StringField(label='Marca',
                                render_kw={'class': 'form-control',
                                           'placeholder': 'Ingrese la marca'})
    serie_producto = wtforms.StringField(label='Serie del producto',
                                render_kw={'class': 'form-control',
                                           'placeholder': 'Ingrese la marca'})
    modelo_producto = wtforms.StringField(label='Modelo dle producto',
                                render_kw={'class': 'form-control',
                                           'placeholder': 'Ingrese la marca'})
    precio = wtforms.DecimalField(label='Precio del producto', default=0.0,
                                  render_kw={'class': 'form-control',
                                             'placeholder': 'Ingrese el precio del producto'})
    descripcion = wtforms.TextAreaField(label='Ingrese una descripcion', default="Sin descripcion",
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese una descripcion'})

    activo = wtforms.BooleanField(label='Activo', default=True)

    estados_id = wtforms.SelectField(label="Estados", coerce=str, choices=[(0, '-------')],
                                     render_kw={'class': 'form-control'}, default=0)

    image = wtforms.FileField(label="Imagen", render_kw={'class': 'form-control'})

    categoria_id = wtforms.SelectField(label="Categorias", coerce=str, choices=[(0, '-------')],
                                       render_kw={'class': 'form-control'}, default=0)
    medida_id = wtforms.SelectField(label="Medida", coerce=str, choices=[(0, '-------')],
                                    render_kw={'class': 'form-control'}, default=0)

    def set_codigo_id(self, lista):
        if len(lista):
            self.estados_id.choices = self.estados_id.choices + lista

    def set_categoria_id(self, lista):
        if len(lista):
            self.categoria_id.choices = self.categoria_id.choices + lista

    def set_medida_id(self, lista):
        if len(lista):
            self.medida_id.choices = self.medida_id.choices + lista

    # def validate_estados_id(self, field):
    #     value = int(field.data)
    #     if value == 0:
    #         field.data = None

    def validate_categoria_id(self, field):
        print("validate_categoria_id")
        value = int(field.data)
        if value == 0:
            print('validate_categoria_id erro')
            raise vt.ValidationError("Debe seleccionar la categoria que pertenece el producto")


class UniadesDeMedidaForm(FlaskForm):
    codigo = wtforms.StringField(label='Codigo de medida', validators=[vt.DataRequired(), vt.Length(max=50)],
                                 render_kw={'class': 'form-control',
                                            'placeholder': 'Ingrese el codigo de la medida'})
    nombre_unidad = wtforms.StringField(label='Nombre de Unidad', validators=[vt.DataRequired(), vt.Length(max=50)],
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese el nombre de la unidad'})
    activo = wtforms.BooleanField(label='Activo', default=True)
