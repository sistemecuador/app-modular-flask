from flask import render_template
from flask_login import login_required
from flask_mail import Message, Mail
from markupsafe import Markup

from config.settings import Config
from . import home
from ..tickets.models import TicketsSalida

mail = Mail()


@home.route("/inicio", methods=['GET'])
@login_required
def inicio():
    query = TicketsSalida.query.get(11)
    productos = query.tt_productos
    context = {
        'Title': 'Home',
        'productos': productos,
    }
    try:
        svg = open(r'C:\Users\isaac\Desktop\desarrollos_flask\app_modular\utils\qr_code\prueba.svg')
        file = svg.readlines()
        svg_qr = ''
        print("tipo", type(file))
        for f in file:
            svg_qr += f
        context['svg'] = Markup(svg_qr)
        # msg = Message('Gracias por tu registro', sender=Config.MAIL_USERNAME, recipients=['isaac-99@hotmail.es'])
        # msg.html = render_template('reporte.html', context=context)
        # mail.send(msg)
    except Exception as e:
        print("Error", str(e))
    print(context)
    return render_template("reporte.html", context=context)
