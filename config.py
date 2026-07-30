import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_change_me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Upload folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # Storage Configuration
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER', 'local')
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(Config.BASE_DIR, 'instance', 'birthday.db')}"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
    @property
    def SECRET_KEY(self):
        val = os.environ.get('SECRET_KEY')
        if not val or val == 'default_secret_key_change_me':
            raise ValueError("SECRET_KEY environment variable is required in production!")
        return val

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required in production!")
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
