from flask import render_template, request, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename, redirect

from apps.inventario.apps.categorias.models import Categorias
from apps.inventario.apps.estados.models import EstadosProductos
from apps.inventario.apps.productos import products
from apps.inventario.apps.productos.forms import ProductosForm, UniadesDeMedidaForm
from apps.inventario.apps.productos.models import Productos, UnidadDeMedida


@products.route("/list")
@login_required
def list_products():
    print("Hola")
    query = Productos.get_all()
    context = {
        'title': 'Productos',
        'title_card': 'Lista de productos',
        'productos': query
    }
    return render_template('productos/list.html', context=context, add_productos=url_for("productos.add_products"))


@products.route("/add", methods=['GET', 'POST'])
@login_required
def add_products():
    query_estados = EstadosProductos.get_query_all()
    query_categorias = Categorias.get_query_all()
    query_medidad = UnidadDeMedida.get_query_all()
    form = ProductosForm()
    form.set_codigo_id(query_estados)
    form.set_categoria_id(query_categorias)
    form.set_medida_id(query_medidad)
    context = {'title': 'Agregar categorias',
               'title_card': 'Agregar categoria',
               'form': form}
    if form.validate_on_submit():
        try:
            image = secure_filename(form.image.data.filename)
            file = form.image.data
            fecha_ingreso = form.fecha_ingreso.data
            nombre_producto = form.name_producto.data
            marca = form.marca.data
            precio = form.precio.data
            codigo = form.codigo_producto.data
            modelo_producto = form.modelo_producto.data
            serie_producto = form.serie_producto.data
            activo = form.activo.data
            estado_id = None if int(form.estados_id.data) == 0 else form.estados_id.data
            categoria_id = form.categoria_id.data
            medida_id = form.medida_id.data if int(form.medida_id.data) != 0 else None
            descripcion = form.descripcion.data
            producto = Productos(fecha_ingreso=fecha_ingreso, name_producto=nombre_producto, codigo_producto=codigo,
                                 modelo_producto=modelo_producto, serie_producto=serie_producto, estados_id=estado_id,
                                 categoria_id=categoria_id, medida_id=medida_id,
                                 descripcion=descripcion, activo=activo, marca=marca, precio=precio)
            producto.save()
            if image != '':
                filename_image = f'{producto.id}-{image}'
                producto.image = filename_image
                path = Productos.crear_directorio(filename=filename_image)
                file.save(path)
            producto.generate_unix_time()
            producto.save()
            return redirect(url_for("productos.list_products"))
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    return render_template("productos/add.html", context=context)


@products.route("/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_products(pk):
    producto = Productos.query.get_or_404(pk)
    query_estados = EstadosProductos.get_query_all()
    query_categorias = Categorias.get_query_all()
    query_medidad = UnidadDeMedida.get_query_all()
    form = ProductosForm(obj=producto)
    form.set_codigo_id(query_estados)
    form.set_categoria_id(query_categorias)
    form.set_medida_id(query_medidad)
    context = {'title': 'Agregar categorias',
               'title_card': 'Agregar categoria',
               'form': form}
    if form.validate_on_submit():
        try:
            image = secure_filename(form.image.data.filename)
            file = form.image.data
            fecha_ingreso = form.fecha_ingreso.data
            nombre_producto = form.name_producto.data
            marca = form.marca.data
            precio = form.precio.data
            codigo = form.codigo_producto.data
            modelo_producto = form.modelo_producto.data
            serie_producto = form.serie_producto.data
            activo = form.activo.data
            estado_id = None if int(form.estados_id.data) == 0 else form.estados_id.data
            categoria_id = form.categoria_id.data
            medida_id = form.medida_id.data if int(form.medida_id.data) != 0 else None
            descripcion = form.descripcion.data
            old_path_image = producto.get_path_file()
            pro = producto.set_obj(fecha_ingreso=fecha_ingreso, name_producto=nombre_producto, codigo_producto=codigo,
                                   estados_id=estado_id, modelo_producto=modelo_producto, serie_producto=serie_producto,
                                   categoria_id=categoria_id, medida_id=medida_id, descripcion=descripcion,
                                   activo=activo, marca=marca, precio=precio)
            if image != '':
                print("old_path_image", old_path_image)
                filename_image = f'{producto.id}-{image}'
                path = Productos.crear_directorio(filename=filename_image)
                pro.image = filename_image
                file.save(path)
                Productos.remove_file(old_path_image)
            pro.save()
            return redirect(url_for("productos.list_products"))
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    return render_template("productos/add.html", context=context)


@products.route("/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_products(pk):
    producto = Productos.query.get_or_404(pk)
    message = "Al eliminar este producto, se eliminaran todos los datos que se correlacionan"
    context = {'title': 'Eliminar producto',
               'title_card': 'Eliminacion de producto',
               'form': '',
               'obj': producto,
               'message': message
               }

    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                producto.delete()
                image = producto.image
                path = producto.get_path_file()
                producto.remove_file(path)
                return redirect(url_for('productos.list_products'))
    except Exception as e:
        flash(str(e))
    return render_template("productos/delete.html", context=context)


@products.route("/medidas/list")
@login_required
def list_medidas():
    print("Hola")
    query = UnidadDeMedida.get_all()
    context = {
        'title': 'Medidas',
        'title_card': 'Lista de medidas',
        'medidas': query
    }
    return render_template('productos/medidas/list.html', context=context, add_medidas=url_for("productos.add_medidas"))


@products.route("/medidas/add", methods=['GET', 'POST'])
@login_required
def add_medidas():
    form = UniadesDeMedidaForm()
    context = {'title': 'Agregar categorias',
               'title_card': 'Agregar categoria',
               'form': form}
    if form.validate_on_submit():
        try:
            codigo = form.codigo.data
            nombre_unidad = form.nombre_unidad.data
            activo = form.activo.data
            medida = UnidadDeMedida.query.filter_by(codigo=codigo).first()
            if not medida:
                medida = UnidadDeMedida(codigo, nombre_unidad, activo)
                medida.save()
                return redirect(url_for("productos.list_medidas"))
            else:
                flash("El codigo de la unidad de medida ya existe")
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    return render_template("productos/medidas/add.html", context=context)


@products.route("/medidas/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_medidas(pk):
    medida = UnidadDeMedida.query.get_or_404(pk)
    form = UniadesDeMedidaForm(obj=medida)

    context = {'title': 'Editar medidas',
               'title_card': 'editar medidas',
               'form': form}
    if form.validate_on_submit():
        try:
            codigo_form = form.codigo.data
            codigo_obj = medida.codigo
            if codigo_form == codigo_obj:
                form.populate_obj(obj=medida)
                medida.save()
                return redirect(url_for("productos.list_medidas"))
            else:
                unid_medida = UnidadDeMedida.query.filter_by(codigo=codigo_form).first()
                if not unid_medida:
                    form.populate_obj(obj=medida)
                    medida.save()
                    return redirect(url_for("productos.list_medidas"))
                flash("El codigo de la unidad de medida ya existe")
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    return render_template("productos/medidas/add.html", context=context)


@products.route("/medidas/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_medidas(pk):
    medida = UnidadDeMedida.query.get_or_404(pk)
    message = "Al eliminar este producto, se eliminaran todos los datos que se correlacionan"
    context = {'title': 'Eliminar unidad de medida',
               'title_card': 'Eliminacion de unidad de medida',
               'form': '',
               'obj': medida,
               'message': message
               }

    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                medida.delete()
                return redirect(url_for('productos.list_medidas'))
    except Exception as e:
        flash(str(e))
    return render_template("productos/medidas/delete.html", context=context)
