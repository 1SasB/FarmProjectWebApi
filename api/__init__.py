from flask import Flask
from flask_pymongo import PyMongo
from datetime import datetime as date
from os import path
# from flask_talisman import Talisman
# from flask_babel import Babel
from flask_mail import Mail

if path.exists("env.py"):
    import env

mongo = PyMongo()

mail = Mail()

def create_app(config_env=""):
    app = Flask(__name__)

    
    if not config_env:
        config_env = app.env
    app.config.from_object(f"config.{config_env.capitalize()}Config")


    mongo.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from api.main.views import main
        app.register_blueprint(main) 

    from api.auth.views import auth
    app.register_blueprint(auth) 
    from api.farm.views import project
    app.register_blueprint(project) 
    
    

    return app
