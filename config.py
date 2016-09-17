import os
from urllib.parse import urlparse

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
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        with app.app_context():
            from app.models import db
            from app.models import User, Notebook

            db.init_app(app)
            db.create_all()

            # Check if User Already Created
            u = User.query.filter_by(email='admin@example.com').first()
            if u:
                pass
            else:
                # Create Admin User
                u = User(
                    email='admin@example.com', password='password',
                    confirmed=True)
                db.session.add(u)
                db.session.commit()

                # Create Default Notebook for Admin User
                nb = Notebook(
                    title='Default Notebook',
                    author_id=u.id)
                db.session.add(nb)
                db.session.commit()


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}@{1}/{2}'.format(
        'ubuntu',
        'localhost',
        'circle_test')


class ProductionConfig(Config):
    url = urlparse(os.environ["DATABASE_URL"])
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
        url.username,
        url.password,
        url.hostname,
        url.path[1:])

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
