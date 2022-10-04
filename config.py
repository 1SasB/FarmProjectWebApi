""" Configuration file """
from datetime import timedelta
# from distutils.debug import DEBUG
import os
from os import environ, path
# from dotenv import load_dotenv


# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config(object):

    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
    # app.config['SECRET_KEY'] = SECRET_KEY
    # app.config['MAIL_DEFAULT_SENDER'] = "sasuyeboahbenjamin@gmail.com"
    # app.config['SECURITY_PASSWORD_SALT'] = "sdfsd./sdfsd"
    # app.config['MAIL_PASSWORD'] = 'ooayivfqewxkeuqm'
    # app.config['MAIL_USERNAME'] = "sasuyeboahbenjamin@gmail.com"

    # DATABASE_URL=os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/FarmDatabase'

    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True


    DEBUG = False
    TESTING = False
    SECRET_KEY = 'f@rm&ji9)/opsd45sd' 
    SECURITY_PASSWORD_SALT = "sdfsd./sdfsd"
    MONGO_URI = os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/FarmDatabase'
    PERMANENT_SESSION_LIFETIME =  timedelta(minutes=15)
    LANGUAGES = ['en','fr']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'sasuyeboahbenjamin@gmail.com'
    # MAIL_PASSWORD = 'ooayivfqewxkeuqm'
    MAIL_PASSWORD = 'oskqharrilnllprq'

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # BABEL_DEFAULT_LOCALE = 'en'


class ProductionConfig(Config):
    MONGO_DBNAME = 'FarmDatabase'


class DevelopmentConfig(Config):
    MONGO_DBNAME = 'FarmDatabase'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True