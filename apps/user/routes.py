from flask import render_template
from flask_login import login_required

from . import app_user
from config.db import db
from apps.user.models import User


@app_user.route("/users")
@login_required
def users():
    error = ''
    try:
        pass
        # user = User(username='isaac2', password='1234567', email='isaac@gmail.com')
        # user.save()
    except Exception as e:
        error = str(e)
    return render_template("user/user.html", error=error)


@app_user.route("/users/edit/<int:pk>")
@login_required
def user_edit(pk):
    error = ''
    try:
        user = User.query.get_or_404(pk)
        user.email = 'isaac46@gmail.com'
        user.save()
    except Exception as e:
        print("Error", str(e))
        error = str(e)
    return render_template("user/user.html", error=error)
