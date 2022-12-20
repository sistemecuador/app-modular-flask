from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required

from . import departamentos
from .forms import DepartamentosForm
from .models import Departamentos


@departamentos.route("/list")
@login_required
def list_departamentos():
    query = Departamentos.get_all()
    context = {
        'title': 'Departamentos',
        'title_card': 'Lista de departamentos',
        'departamentos': query
    }
    return render_template('departamentos/list.html', context=context,
                           url_add=url_for("departamentos.add_departamentos"))


@departamentos.route("/add", methods=['GET', 'POST'])
@login_required
def add_departamentos():
    form = DepartamentosForm()
    context = {'title': 'Agregar departamentos',
               'title_card': 'Agregar departamento',
               'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            nombre_departamento = form.nombre_departamento.data
            observacion = form.observacion.data
            activo = form.activo.data
            try:
                depa = Departamentos(nombre_departamento=nombre_departamento, observacion=observacion, activo=activo)
                depa.save()
                return redirect(url_for('departamentos.list_departamentos'))
            except Exception as e:
                flash(str(e))
    return render_template("departamentos/add.html", context=context)


@departamentos.route("/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_departamentos(pk):
    depa = Departamentos.query.get_or_404(pk)
    form = DepartamentosForm(obj=depa)
    context = {'title': 'Editar departamentos',
               'title_card': 'Editar departamento',
               'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(obj=depa)
            try:
                depa.save()
                return redirect(url_for('departamentos.list_departamentos'))
            except Exception as e:
                flash(str(e))
    return render_template("departamentos/add.html", context=context)


@departamentos.route("/list/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_departamentos(pk):
    message = "Al eliminar este registro, se eliminaran los datos dependientes de este"
    depa = Departamentos.query.get_or_404(pk)
    context = {'title': 'Eliminar departamentos',
               'title_card': 'Eliminar departamento',
               'form': '',
               'obj': depa,
               'message': message}
    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                depa.delete()
                return redirect(url_for('departamentos.list_departamentos'))
    except Exception as e:
        flash(str(e))
    return render_template("departamentos/delete.html", context=context)
