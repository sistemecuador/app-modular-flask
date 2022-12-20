from flask import redirect, url_for, render_template, flash
from flask_login import login_required

from . import personal
from .forms import PersonalForm
from .models import *
from ..departamentos.models import Departamentos


@personal.route("/list")
@login_required
def list_personal():
    query = Personal.get_all()
    context = {
        'title': 'Personal',
        'title_card': 'Lista de personal',
        'personal': query
    }
    return render_template('personal/list.html', context=context)


@personal.route("/add", methods=['GET', 'POST'])
@login_required
def add_personal():
    lista_departamentos = Departamentos.get_list_all()
    form = PersonalForm()
    form.set_id_departamentos(lista_departamentos)
    context = {'title': 'Agregar Personal',
               'title_card': 'Agregar personal',
               'form': form}
    if form.validate_on_submit():
        try:
            nombre_personal = form.nombre_completo.data
            identificador = form.identificador.data
            correo = form.correo.data
            activo = form.activo.data
            id_departamento = form.id_departamento.data
            contacto = form.contacto.data
            person = Personal.query.filter_by(identificador=identificador).first()
            if not person:
                person = Personal(nombre_completo=nombre_personal, identificador=identificador, correo=correo,
                                  activo=activo,
                                  id_departamento=id_departamento, contacto=contacto)
                person.save()
                return redirect(url_for("personal.list_personal"))
            else:
                flash("Ys existe un identificador con ese dato")
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    else:
        print(form.errors)
    return render_template("personal/add.html", context=context)


@personal.route("/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_personal(pk):
    person = Personal.query.get_or_404(pk)
    lista_departamentos = Departamentos.get_list_all()
    form = PersonalForm(obj=person)
    form.set_id_departamentos(lista_departamentos)
    context = {'title': 'Editar Personal',
               'title_card': 'Editar personal',
               'form': form}
    if form.validate_on_submit():
        try:
            identificador_form = form.identificador.data
            identificador_obj = person.identificador
            if identificador_obj == identificador_form:
                form.populate_obj(obj=person)
                person.save()
                return redirect(url_for("personal.list_personal"))
            else:
                flash("Ys existe un identificador con ese dato")
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    else:
        print(form.errors)
    return render_template('personal/add.html', context=context)


@personal.route("/list/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_personal(pk):
    return 'lista'
