from flask import render_template
from flask_mail import Mail, Message

from config.settings import Config

mail = Mail()


def notificar_usuario(asunto, context, recipients=[]):
    msg = Message(asunto, sender=Config.MAIL_USERNAME, recipients=recipients)
    msg.html = render_template('notificacion/reporte.html', context=context)
    mail.send(msg)
