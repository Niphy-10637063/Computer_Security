from flask import Flask
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS
from src.database import db
from src.auth import auth
from src.user import user
from datetime import timedelta

def create_app(test_config=None):

    app=Flask(__name__,instance_relative_config=True)
    CORS(app,supports_credentials=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
        )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    return app


