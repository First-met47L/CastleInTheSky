import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[CastleInTheSky]'
    FLASK_MAIL_SENDER = 'CastleInTheSky Admin <{mail_username}>'.format(mail_username=os.environ.get("MAIL_USERNAME"))
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(Config):
    TESTING = True



class ProductionConfig(Config):
    pass


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}

if __name__ == '__main__':
    print(Config.__dict__)
    print(dir(Config))