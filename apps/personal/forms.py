from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as vt


class PersonalForm(FlaskForm):
    nombre_completo = wtforms.StringField(label='Nombre completo',
                                          validators=[vt.DataRequired(), vt.Length(max=200)],
                                          render_kw={'class': 'form-control',
                                                     'placeholder': 'Ingrese nombres completos'}
                                          )
    identificador = wtforms.StringField(label='Identificador',
                                        validators=[vt.DataRequired(), vt.Length(max=30)],
                                        render_kw={'class': 'form-control',
                                                   'placeholder': 'Ingrese el identificador de la persona'}
                                        )
    contacto = wtforms.StringField(label='Contacto',
                                   validators=[vt.Length(max=30)],
                                   render_kw={'class': 'form-control',
                                              'placeholder': 'Ingrese el contacto'}
                                   )
    correo = wtforms.EmailField(label='Correo',
                                validators=[vt.DataRequired(), vt.Length(max=100), vt.Email()],
                                render_kw={'class': 'form-control',
                                           'placeholder': 'Ingrese el correo'}
                                )
    id_departamento = wtforms.SelectField(label="Departamento",
                                          coerce=str, choices=[(0, '-----')], default=0,
                                          render_kw={'class': 'form-control'})
    activo = wtforms.BooleanField(default=True)

    def set_id_departamentos(self, lista):
        if len(lista):
            self.id_departamento.choices = self.id_departamento.choices + lista

    def validate_id_departamento(self, field):
        value = field.data
        if int(value) == 0:
            field.data = None
