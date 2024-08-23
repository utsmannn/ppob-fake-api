from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_jwt_extended import JWTManager
from flask_restful import abort

from app.config import config
from app.routes import v1_bp

class CustomJSONProvider(DefaultJSONProvider):
    sort_keys = False


jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.json = CustomJSONProvider(app)
    app.config['JWT_SECRET_KEY'] = 'utsmankecebadai'
    jwt.init_app(app)

    app.register_blueprint(v1_bp)
    return app

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    abort(401, message='Token expires', status=False)

@jwt.unauthorized_loader
def unauthorized_callback(jwt_header):
    abort(401, message='Unauthorized', status=False)

@jwt.invalid_token_loader
def invalid_payload_callback(jwt_header):
    abort(401, message='Token invalid!', status=False)