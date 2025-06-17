from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['JWT_SECRET_KEY'] = 'mihajlo_marjanovic'

    db.init_app(app)
    jwt.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app