import os.path

from flask import redirect, url_for, send_from_directory
from flask_login import login_required

from apps.inventario import inventario
from config.constantes import UPLOAD_FOLDER


@inventario.route("/list")
@login_required
def list_inventario():
    return redirect(url_for("estados.list_estados"))


@inventario.route("/uploads/<sub_directorio>/<path:filename>")
@inventario.route("/uploads/<path:filename>")
@login_required
def uploads(filename, sub_directorio=None):
    ruta = ''
    file = filename
    if sub_directorio is None:
        path = os.path.join(UPLOAD_FOLDER)
    else:
        ruta = os.path.join(UPLOAD_FOLDER, f'{sub_directorio}')
    print(ruta, file)
    if not os.path.exists(os.path.join(ruta, file)):
        return redirect(url_for('static', filename='img/empty.png'))
    return send_from_directory(
        ruta, file, as_attachment=True
    )
