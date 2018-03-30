from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap ()
mail = Mail ()
moment = Moment ()
db = SQLAlchemy ()
login_manager = LoginManager ()
# LoginManager 对象的 session_protection 属性可以设为 None 、 'basic' 或 'strong'
# 设为 'strong' 时,Flask-Login 会记录客户端 IP地址和浏览器的用户代理信息,如果发现异动就登出用户。
login_manager.session_protection = 'strong'
# set login page's endpoint
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask (__name__)
    config_object = config.get (config_name)
    if not config_object:
        raise AttributeError ("config_name isn't in config dictionary")
    app.config.from_object (config_object)
    config_object.init_app (app=app)

    login_manager.init_app (app)
    bootstrap.init_app (app)
    mail.init_app (app)
    moment.init_app (app)
    db.init_app (app)
    from .main import main as main_blueprint
    app.register_blueprint (blueprint=main_blueprint)
    from .auth import auth as  auth_blueprint
    app.register_blueprint (blueprint=auth_blueprint, url_prefix='/auth')
    # app.register_blueprint (blueprint=auth_blueprint, url_prefix='/auth')

    return app
