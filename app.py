import sys

from flask_mail import Mail
from flask_migrate import Migrate

from base.auth.login import login_manager
from base.contrib.models import AnonymousUserMixin
from config.app import create_app
from config.db import db

app = create_app()

migrate = Migrate(app, db)
migrate.init_app(app)
login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUserMixin
mail = Mail()
mail.init_app(app)
if __name__ == '__main__':
    app.run()

from base.command.utils.util import CommandBase
