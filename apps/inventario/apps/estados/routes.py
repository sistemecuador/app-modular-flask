from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from apps.inventario.apps.estados import estados
from apps.inventario.apps.estados.forms import EstadosForm
from apps.inventario.apps.estados.models import EstadosProductos


@estados.route("/list")
@login_required
def list_estados():
    query = EstadosProductos.get_all()
    context = {'title': 'Estados',
               'title_card': 'Lista de estado',
               'estados': query}
    return render_template("estados/list.html", context=context, add_registro=url_for("estados.add_estados"))


@estados.route("/add", methods=['GET', 'POST'])
@login_required
def add_estados():
    form = EstadosForm()
    context = {'title': 'Agregar Estado',
               'title_card': 'Agregar Estados',
               'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            nombre = form.nombre_estado.data
            activo = form.activo.data
            try:
                estado = EstadosProductos.query.filter_by(nombre_estado=nombre).first()
                if not estado:
                    estado = EstadosProductos(nombre_estado=nombre, activo=activo)
                    estado.save()
                    return redirect(url_for('estados.list_estados'))
                else:
                    flash("El nombre del estado ya existe")
            except Exception as e:
                flash(str(e))
    return render_template("estados/add.html", context=context)


@estados.route("/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_estados(pk):
    estado = EstadosProductos.query.get_or_404(pk)
    form = EstadosForm(obj=estado)
    context = {'title': 'Agregar Estado',
               'title_card': 'Agregar Estados',
               'form': form}

    if request.method == 'POST':
        if form.validate_on_submit():
            try:

                query = EstadosProductos.query.filter_by(nombre_estado=form.nombre_estado.data).first()
                if not query:
                    form = form.populate_obj(obj=estado)
                    estado.save()
                    return redirect(url_for('estados.list_estados'))
                else:
                    flash("El nombre del estado ya existe")
            except Exception as e:
                flash(str(e))
    return render_template("estados/add.html", context=context)


@estados.route("/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_estados(pk):
    message = "Al eliminar este registro, se eliminaran los datos dependientes de este"
    estados = EstadosProductos.query.get_or_404(pk)
    context = {'title': 'Eliminar estado',
               'title_card': 'Eliminar estado',
               'form': '',
               'obj': estados,
               'message': message}
    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                estados.delete()
                return redirect(url_for('estados.list_estados'))
    except Exception as e:
        flash(str(e))
    return render_template("estados/delete.html", context=context)
