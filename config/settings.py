from config.constantes import UPLOAD_FOLDER


class Config(object):
    # SERVER_NAME = '0.0.0.0:5000'
    DEBUG = True
    SECRET_KEY = 'kjasgsjgsjdgjsdkkjsdjhgsdhgdsjjkhi72672jd;lbh'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'apps.py'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'isaacbo841@gmail.com'
    MAIL_PASSWORD = 'iqachedryqdpuesl'
    DONT_REPLY_FROM_EMAIL = '(Isaac, isaacbo841@gmail.com)'
    ADMINS = ('isaacbo841@gmail.com',)


class ProductionConfig(Config):
    DEBUG = False
    #DATABASE_URI = 'mysql://user@localhost/foo'
    #SERVER_NAME = '172.18.55.6'
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:Nomeacuerdo123.@ins-db-flask.cmbbdayqxe6k.us-east-1.rds.amazonaws.com:5432/inventario'


class DevelopmentConfig(Config):
    # SERVER_NAME = 'localhost:3000'
    # SQLALCHEMY_DATABASE_URI = f'mysql://root:Nomeacuerdo123.@localhost:3306/flask'
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:Nomeacuerdo123.@ins-db-flask.cmbbdayqxe6k.us-east-1.rds.amazonaws.com:5432/inventario'
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR_P}/apps.db'


class TestingConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:Nomeacuerdo123.@ins-db-flask.cmbbdayqxe6k.us-east-1.rds.amazonaws.com:5432/inventario'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
