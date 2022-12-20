import os

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from apps.inventario.apps.categorias import categorias
from apps.inventario.apps.categorias.forms import CategoriasForm
from apps.inventario.apps.categorias.models import Categorias


@categorias.route("/list")
@login_required
def list_categorias():
    query = Categorias.get_all()
    context = {
        'title': 'Categorias',
        'title_card': 'Lista de categorias',
        'categorias': query
    }
    return render_template("categorias/list.html", context=context, add_categorias=url_for("categorias.add_categorias"))


@categorias.route("/add", methods=['GET', 'POST'])
@login_required
def add_categorias():
    form = CategoriasForm()
    context = {'title': 'Agregar categorias',
               'title_card': 'Agregar categoria',
               'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            nombre_categoria = form.nombre_categoria.data
            activo = form.activo.data
            image = secure_filename(form.image.data.filename)
            descripcion = form.descripcion.data
            try:
                categoria = Categorias.query.filter_by(nombre_categoria=nombre_categoria).first()
                if not categoria:
                    categoria = Categorias(nombre_categoria=nombre_categoria, activo=activo, descripcion=descripcion)
                    categoria.save()
                    if image != '':
                        filename = f'{str(categoria.id)}-{image}'
                        categoria.image = filename
                        path = Categorias.crear_directorio(filename=filename)
                        form.image.data.save(path) if image != '' else None
                    categoria.save()
                    return redirect(url_for('categorias.list_categorias'))
                else:
                    flash("La categorias ya existe")
            except Exception as e:
                flash(str(e))
    return render_template("categorias/add.html", context=context)


@categorias.route("/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_categorias(pk):
    categoria = Categorias.query.get_or_404(pk)
    form = CategoriasForm(obj=categoria)
    context = {'title': 'Editar categorias',
               'title_card': 'Editar categoria',
               'form': form}

    if request.method == 'POST':
        if form.validate_on_submit():
            nombre_categoria = form.nombre_categoria.data
            activo = form.activo.data
            image = secure_filename(form.image.data.filename)
            descripcion = form.descripcion.data
            try:
                old_nombre_cat = categoria.nombre_categoria
                if old_nombre_cat != nombre_categoria:
                    q_categoria = Categorias.query.filter_by(nombre_categoria=nombre_categoria).first()
                    if q_categoria:
                        flash("La categorias ya existe")
                        return render_template("categorias/add.html", context=context)
                categoria.nombre_categoria = nombre_categoria
                categoria.activo = activo
                categoria.descripcion = descripcion
                if image != '':
                    new_image = f'{str(categoria.id)}-{image}'
                    # old_image = categoria.image
                    old_path = categoria.get_path_file()
                    categoria.image = new_image
                    path = Categorias.crear_directorio(filename=new_image)
                    categoria.remove_file(old_path)
                    form.image.data.save(path)
                categoria.save()
                return redirect(url_for('categorias.list_categorias'))
            except Exception as e:
                print("Error", str(e))
                flash(str(e))
        else:
            print(form.errors)
    return render_template("categorias/add.html", context=context)


@categorias.route("/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_categorias(pk):
    message = "Al eliminar este registro, se eliminaran los datos dependientes de este"
    categoria = Categorias.query.get_or_404(pk)
    context = {'title': 'Eliminar categorias',
               'title_card': 'Eliminar categoria',
               'form': '',
               'obj': categoria,
               'message': message}
    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                categoria.delete()
                image = categoria.image
                path = categoria.get_path_file()
                categoria.remove_file(path) if image != '' else None
                return redirect(url_for('categorias.list_categorias'))
    except Exception as e:
        flash(str(e))
    return render_template("categorias/delete.html", context=context)
