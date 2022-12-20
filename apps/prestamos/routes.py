import datetime
from flask import render_template, request, jsonify, Response, redirect, url_for, current_app
import json

from flask_login import login_required

from base.notificacion_mail.notificacion import send_email
from base.status_code import HTTP_404_NOT_FOUND
from config.db import db
from . import prestamos
from .forms import FormBuscarProducto, ResponsableForm, TicketForm
from .helpers import GuardarDatosForms
from ..departamentos.models import Departamentos
from ..inventario.apps.productos.models import Productos
from ..personal.models import Personal
from ..tickets.models import TicketsSalida


@prestamos.route("/registro", methods=['GET', 'POST'])
@login_required
def registros():
    method = request.method
    form_buscar_producto = FormBuscarProducto()
    form_responsable = ResponsableForm()
    ticket_form = TicketForm()
    ticket_form.set_departamentos_choice(Departamentos.get_list_all())
    context = {
        'form_buscar_producto': form_buscar_producto,
        'form_responsable': form_responsable,
        'ticket_form': ticket_form
    }
    data = {}
    if method == 'GET':
        print(request.headers)
        return render_template('prestamos/registros.html', context=context)
    else:
        try:
            print(request.headers)
            datos = request.form
            action = datos.get("action", None)
            if action == 'list_productos':
                lista = []
                query = Productos.query.all()
                for item in query:
                    lista.append(item.as_dict(exclude=['date_create', 'date_update', 'user_create', 'user_update']))
                data = {
                    'nombre': 'isaac',
                    'data': lista
                }
            elif action == 'buscar_productos':
                codigo_de_barra = datos.get("codigo_producto")
                query = Productos.query.filter_by(codigo_de_barra=codigo_de_barra, activo=True).first()
                if query:
                    data = query.as_dict(exclude=['date_create', 'date_update', 'user_create', 'user_update'])
                    data['estados_productos'] = query.estados_productos.get_query_all()
                else:
                    data = {
                        'error': 'El producto no esta disponible o no existe'
                    }
            elif action == 'buscar_responsable':
                if form_responsable.validate_on_submit():
                    identificador = form_responsable.identificador.data
                    query = Personal.query.filter_by(identificador=identificador).first()
                    if query:
                        departamento = query.departamentos_personal
                        data = query.as_dict(exclude=['date_create', 'date_update', 'user_create', 'user_update'])
                        data[
                            'name_departamento'] = departamento.nombre_departamento if departamento is not None else None
                    else:
                        data = {
                            'error': 'No se encontro a la persona'
                        }
                else:
                    print("Error form_responsable", form_responsable.errors)
                    data = {'error': 'El formulario esta incorrecto', 'validate_form': form_responsable.errors}
            elif action == 'generar_tt':
                if ticket_form.validate_on_submit():
                    dni = ticket_form.dni.data
                    nombres = ticket_form.nombres.data
                    contacto = ticket_form.contacto.data
                    correo = ticket_form.correo.data
                    observacion = ticket_form.observacion.data
                    total_p = ticket_form.total_p.data
                    list_productos = json.loads(request.form.get('list_productos'))
                    object_productos = GuardarDatosForms.save_model_productos(Productos, list_productos)
                    instancia_responsable = Personal.query.filter_by(identificador=dni).first()
                    responsable = GuardarDatosForms.save_model_personal(instancia_responsable, contacto, correo)
                    fecha_salida = datetime.date.today()
                    instancia_tt = TicketsSalida(fecha_salida=fecha_salida, obs_salida=observacion,
                                                 estado_salida=True,
                                                 activo=True, id_personal=instancia_responsable.id)
                    data_tt_salida = GuardarDatosForms.save_model_tt_salida(instancia_tt, responsable, object_productos)
                    data = data_tt_salida
                    email = responsable.correo
                    if data_tt_salida:
                        context = {'responsable': responsable,
                                   'tt': {'tt_salida': data_tt_salida['tt_salida'], 'total': total_p},
                                   'productos': object_productos, 'date': datetime.date.today().strftime('%Y-%m-%d'),
                                   'ti': {'full_name': 'Isaac Briceño', 'contacto': '0989227122',
                                          'correo': 'ibriceno@sistemecuador.com'}}
                        template = render_template('notificacion/reporte.html', context=context)
                        send_email(subject='PRESTAMO DE RECURSOS SISTEMAS DE COBRO DEL ECUADOR S.A.',
                                   sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                                   recipients=[email, ],
                                   cc=['isalazar@sistemecuador.com', 'isaac-99@hotmail.es',
                                       'jsantos@sistemecuador.com'],
                                   text_body=f'Este es un mensaje automatico, generado para informar sobre los recursos prestados en la empresa',
                                   html_body=template)
                else:
                    print("error", ticket_form.errors)
                    data = {'error': 'El formulario esta incorrecto', 'validate_form': ticket_form.errors}
            else:
                data = {
                    'error': 'No se ha encobtrado la accion'
                }
        except Exception as e:
            print("Error", str(e))
            data = {
                'error': str(e),
            }
        return Response(response=json.dumps(data), content_type='application/json')
