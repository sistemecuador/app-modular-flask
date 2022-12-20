import json

from flask import render_template, request, flash, redirect, url_for, Response
from apps.login.forms import LoginForm, RegistroForm
from apps.user.models import User
from base.auth.login import login_manager
from flask_login import login_user
from apps.login import login as lg


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@lg.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    method = request.method
    if method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            remember_me = form.remember_me.data
            password = form.password.data
            if user:
                if user.check_password(password):
                    print("esta correctp")
                    login_user(user, remember=remember_me)
                    return 'Ingresaste al sistema'
                flash("Usuario o clave son incorrectosl", category='info')
            else:
                flash("Usuario no esta registrado", category='info')
    return render_template('login/login.html', form=form)


@lg.route("/registro", methods=['GET', 'POST'])
def registros():
    form = RegistroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            try:
                user = User(username=username, password=password, first_name=first_name, last_name=last_name,
                            email=email)
                user.save()
                flash("Te registraste correctamente")
                return redirect(url_for("login.login"))
            except Exception as e:
                print("error", str(e))
                flash(str(e), category='danger')
        else:
            print(form.errors)
    return render_template('login/registro.html', form=form)
