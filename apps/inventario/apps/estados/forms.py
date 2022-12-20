from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length


class EstadosForm(FlaskForm):
    nombre_estado = wtforms.StringField(label="Nombre del estado", validators=[DataRequired(),Length(max=70)],
                                        render_kw={'class': 'form-control', 'autofocus': 'on', 'autocomplete': 'off',
                                                   'placeholder': 'Ingrese un nombre para el estado'})

    activo = wtforms.BooleanField(label="Activo", default=True)
