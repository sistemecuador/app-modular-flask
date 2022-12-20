from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required

from .forms import TicketsSalidaForm, TicketsCierreForm
from .models import *
from . import tickets
from ..inventario.apps.productos.models import Productos
from ..personal.models import Personal


@tickets.route("/list_salidas")
@login_required
def list_salidas_tt():
    query = TicketsSalida.get_all()
    context = {
        'title': 'Prestamos de recursos',
        'title_card': 'Lista de tickets',
        'tt_salidas': query
    }
    return render_template('tickets/list.html', context=context, add_salidas_tt=url_for("tickets.add_salida_tt"))


@tickets.route("/salida_tt/add", methods=['GET', 'POST'])
@login_required
def add_salida_tt():
    lista_productos = Productos.get_list_all()
    lista_personal = Personal.get_list_all()
    form = TicketsSalidaForm()
    form.set_productos_salida(lista_productos)
    form.set_id_personal(lista_personal)
    context = {'title': 'Registrar salida de productos',
               'title_card': 'Registrar salida de productos',
               'form': form}
    if form.validate_on_submit():
        try:
            fecha_salida = form.fecha_salida.data
            id_personal = form.id_personal.data
            id_productos = form.tt_productos.data
            activo = form.activo.data
            estado_salida = form.estado_salida.data
            observacion_salida = form.observacion_salida.data
            tt = TicketsSalida(fecha_salida=fecha_salida, obs_salida=observacion_salida, estado_salida=estado_salida,
                               activo=activo, id_personal=id_personal)

            for i in id_productos:
                tt.tt_productos.append(Productos.query.get(i))
            tt.save()
            tt.generate_unix_time()
            tt.save()
            return redirect(url_for("tickets.list_salidas_tt"))
        except Exception as e:
            flash(str(e))
            print("Error", str(e))
    return render_template("tickets/add.html", context=context)


@tickets.route("/salida_tt/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_salida_tt(pk):
    tt_salida = TicketsSalida.query.get_or_404(pk)
    list_productos = tt_salida.get_list_products()
    form = TicketsSalidaForm(obj=tt_salida, list_productos=list_productos)
    all_productos = Productos.get_list_all()
    lista_personal = Personal.get_list_all()
    form.set_productos_salida(all_productos)
    form.set_id_personal(lista_personal)
    context = {'title': 'Editar salida de productos',
               'title_card': 'Editar salida de productos',
               'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                tt_salida.fecha_salida = form.fecha_salida.data
                tt_salida.obs_salida = form.observacion_salida.data
                tt_salida.estado_salida = form.estado_salida.data
                tt_salida.activo = form.activo.data
                tt_salida.id_personal = form.id_personal.data
                id_productos = form.tt_productos.data
                for item in list_productos:
                    p = Productos.query.get_or_404(item[0])
                    tt_salida.tt_productos.remove(p)
                for item in id_productos:
                    p = Productos.query.get_or_404(item)
                    tt_salida.tt_productos.append(p)
                tt_salida.save()
                return redirect(url_for("tickets.list_salidas_tt"))
            except Exception as e:
                flash(str(e))
                print("Error", str(e))

    return render_template("tickets/add.html", context=context)


@tickets.route("/salida_tt/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_salida_tt(pk):
    tt_salida = TicketsSalida.query.get_or_404(pk)
    message = "Al eliminar este registro, se eliminaran todos los datos que se correlacionan"
    context = {'title': 'Eliminar tickets',
               'title_card': 'Eliminar ticket de salida',
               'form': '',
               'obj': tt_salida,
               'message': message
               }

    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                tt_salida.delete()
                return redirect(url_for('tickets.list_salidas_tt'))
    except Exception as e:
        flash(str(e))
    return render_template("tickets/delete.html", context=context)



# VISTAS PARA LOS TICKETS DE CIERRE

@tickets.route("/list_cierres")
@login_required
def list_cierres_tt():
    query = TicketsCerrados.query.order_by(TicketsCerrados.id, TicketsCerrados.id_tickets_salida).all()
    context = {
        'title': 'Prestamos de recursos',
        'title_card': 'Lista de cierres de tt',
        'tt_cierres': query
    }
    return render_template('tickets_cierre/list.html', context=context)


@tickets.route("/cierres_tt/add/<int:pk>", methods=['GET', 'POST'])
@login_required
def add_cierres_tt(pk):
    tt_salida = TicketsSalida.query.get(pk)
    productos_entregados = tt_salida.tt_productos
    print("productos entregados", productos_entregados)
    productos_devueltos = Productos.query.join(TicketsCerrados.tt_productos).filter(
        TicketsCerrados.id_tickets_salida == tt_salida.id).all()
    list_productos_entregados = []
    list_productos_devueltos = []
    for p in productos_entregados:
        if p in productos_devueltos:
            list_productos_devueltos.append(p)
        else:
            list_productos_entregados.append(p)
    productos_entregados = [(p.id, p.name_producto) for p in list_productos_entregados]
    tt = tt_salida.get_tt()
    form = TicketsCierreForm()
    form.set_productos_entregados(productos_entregados)
    form.set_id_ticket_salida(tt)
    context = {'title': 'Registrar salida de productos',
               'title_card': 'Registrar salida de productos',
               'form': form}
    if len(productos_entregados) != 0:
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    lista = []
                    fecha_cierre = form.fecha_cierre.data
                    id_tt_salida = form.id_tickets_salida.data
                    id_productos_devueltos = form.tt_productos_devueltos.data
                    activo = form.activo.data
                    estado_cierre = form.estado_cierre.data
                    obs_cierre = form.obs_cierre.data
                    for i in id_productos_devueltos:
                        p = Productos.query.get(i)
                        lista.append(p)
                    tt_cerrado = TicketsCerrados(fecha_cierre=fecha_cierre, obs_cierre=obs_cierre,
                                                 estado_cierre=estado_cierre, activo=activo,
                                                 id_tickets_salida=id_tt_salida)
                    for item in lista:
                        tt_cerrado.tt_productos.append(item)
                    tt_cerrado.save()
                    tt_cerrado.generate_unix_time()
                    tt_cerrado.save()
                    for item in lista:
                        item.activo = False
                        item.save()
                    return redirect(url_for('tickets.list_salidas_tt'))
                except Exception as e:
                    flash(str(e))
                    print("Error", str(e))
            else:
                print(form.errors)
    else:
        flash("El ticket ya no tiene productos pendientes de entrega")
        return redirect(url_for('tickets.list_salidas_tt'))
    return render_template("tickets_cierre/add.html", context=context)


@tickets.route("/cierres_tt/edit/<int:pk>", methods=['GET', 'POST'])
@login_required
def edit_cierres_tt(pk):
    tt_salida = TicketsSalida.query.get_or_404(pk)
    list_productos = [(i.id, i.name_producto) for i in tt_salida.tt_productos]
    form = TicketsSalidaForm(obj=tt_salida, list_productos=list_productos)
    all_productos = Productos.get_list_all()
    lista_personal = Personal.get_list_all()
    form.set_productos_salida(all_productos)
    form.set_id_personal(lista_personal)
    context = {'title': 'Editar salida de productos',
               'title_card': 'Editar salida de productos',
               'form': form}

    return render_template("tickets/add.html", context=context)


@tickets.route("/cierres_tt/delete/<int:pk>", methods=['GET', 'POST'])
@login_required
def delete_cierres_tt(pk):
    tt_cierre = TicketsCerrados.query.get_or_404(pk)
    message = "Al eliminar este registro, se eliminaran todos los datos que se correlacionan"
    context = {'title': 'Eliminar tickets',
               'title_card': 'Eliminar ticket de cierre',
               'form': '',
               'obj': tt_cierre,
               'message': message
               }

    try:
        if request.method == 'POST':
            action = request.form.get("action", None)
            if action == "delete":
                tt_cierre.delete()
                return redirect(url_for('tickets.list_cierres_tt'))
    except Exception as e:
        flash(str(e))
    return render_template("tickets_cierre/delete.html", context=context)
