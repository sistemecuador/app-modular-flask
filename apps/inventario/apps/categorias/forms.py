import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from apps.inventario.apps.categorias.models import Categorias
from config.constantes import UPLOAD_FOLDER
import wtforms
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Length


class CategoriasForm(FlaskForm):
    nombre_categoria = wtforms.StringField(label="Nombre de categoria", validators=[DataRequired(), Length(max=70)],
                                           render_kw={
                                               'placeholder': 'Ingrese el nombre de categoria',
                                               'class': 'form-control'
                                           })
    descripcion = wtforms.TextAreaField(label="Descripcion", validators=[DataRequired(), Length(max=100)], render_kw={
        'placeholder': 'Ingrese una breve descripcion',
        'class': 'form-control'
    })
    image = wtforms.FileField(label='Imagen', validators=[FileAllowed(upload_set=['jpg', 'png'],
                                                                      message="Solamente imagenes")],
                              render_kw={'class': 'form-control'})
    activo = wtforms.BooleanField(label='Activo', default=True)

    def get_files_fields(self):
        lista_filename = []
        lista_file_obj = []
        for item, value in self._fields.items():
            field = value
            if field.type == 'FileField':
                file = getattr(self, field.name).data
                if file.filename != "":
                    filename = secure_filename(file.filename)
                    lista_filename.append(filename)
                    lista_file_obj.append(file)
        return [lista_filename, lista_file_obj]
