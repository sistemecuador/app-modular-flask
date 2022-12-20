from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as vt


class DepartamentosForm(FlaskForm):
    nombre_departamento = wtforms.StringField(
        label='Departamento',
        validators=[vt.DataRequired(), vt.Length(max=50)],
        render_kw={'class': 'form-control', 'placeholder': 'Ingrese el departamento'}
    )
    observacion = wtforms.TextAreaField(
        label='Observacion',
        validators=[vt.DataRequired(), vt.Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Ingrese una observacion', 'value': 'N-A'}
    )
    activo = wtforms.BooleanField('Estado', default=True)
