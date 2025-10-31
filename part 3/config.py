import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'une_clef_secrete_pour_jwt')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
