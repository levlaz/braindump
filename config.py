import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = 'mail.gandi.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[braindump]'
    MAIL_SENDER = 'braindump <noreply@braindump.pw>'
    APP_ADMIN = os.environ.get('BRAINDUMP_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
        'braindump',
        'braindump',
        'localhost',
        'braindump')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}@{1}/{2}'.format(
        'ubuntu',
        'localhost',
        'circle_test')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
        os.environ.get('DB_USER'),
        os.environ.get('DB_PASS'),
        os.environ.get('DB_HOST'),
        os.environ.get('DB_NAME'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
