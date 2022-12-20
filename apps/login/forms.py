from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Length, DataRequired, InputRequired, Email


class LoginForm(FlaskForm):
    username = wtforms.StringField(label="username", validators=[Length(max=20, min=4), DataRequired()],
                                   render_kw={'placeholder': 'username', 'class': 'form-control'})

    password = wtforms.PasswordField(label="password", validators=[Length(max=30, min=4), DataRequired()],
                                     render_kw={'placeholder': 'password', 'class': 'form-control'})

    remember_me = wtforms.BooleanField(label="remember_me", default=True,
                                       render_kw={'placeholder': 'remember_me'})

    enviar = wtforms.SubmitField('enviar', render_kw={'class': 'btn btn-primary'})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def change_class(self, field, update=True, attr='', value='', **kwargs):
        fields = {field: {'attr': {attr: value}}}
        return fields

    def clear_class(self, **kwargs):
        data = self.data
        for item, value in data.items():
            field = getattr(self, item)
            render_kw = getattr(field, 'render_kw', None)
            if render_kw:
                print("render_kw", render_kw)
                print("render_kw type", type(render_kw))
                clase = getattr(render_kw, 'class', None)
                if render_kw.get("class"):
                    valor = field.render_kw.get("class")
                    field.render_kw['class'] = 'form-control'


class RegistroForm(FlaskForm):
    first_name = wtforms.StringField(label="Nombres", validators=[Length(max=100, min=4), DataRequired()],
                                     render_kw={'placeholder': 'Ingrese sus nombres', 'class': 'form-control'})
    last_name = wtforms.StringField(label="Apellidos", validators=[Length(max=100, min=4), DataRequired()],
                                    render_kw={'placeholder': 'Ingrese sus apellidos', 'class': 'form-control'})

    username = wtforms.StringField(label="Username", validators=[Length(max=20, min=4), DataRequired()],
                                   render_kw={'placeholder': 'Ingrese su username', 'class': 'form-control'})

    password = wtforms.PasswordField(label="Password", validators=[Length(max=30, min=4), DataRequired()],
                                     render_kw={'placeholder': 'Ingrese su password', 'class': 'form-control'})

    email = wtforms.EmailField(label="Correo electronico", validators=[Email()],
                               render_kw={'placeholder': 'Ingrese su correo', 'class': 'form-control'})

    register = wtforms.SubmitField('Registrarse', render_kw={'class': 'btn btn-primary btn-block'})

    # def __init__(self, instance=**kwargs):
    #     super(RegistroForm, self).__init__(**kwargs)
