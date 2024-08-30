from flask import Blueprint
from flask_restful import Api

from src.routes.root.root import RootResources

root_bp = Blueprint('root', __name__)
api_root = Api(root_bp)

api_root.add_resource(RootResources, '/qris')