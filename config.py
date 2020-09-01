import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'q1w2e3r4t5y6'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_ADMIN = os.environ.get('APP_ADMIN') or 'admin@app.com'

    @staticmethod
    def init_app(app):
        pass

class DeveplopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir , 'devdata.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir , 'testdata.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir , 'proddata.sqlite')

config = {
    'development' : DeveplopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DeveplopmentConfig
}
