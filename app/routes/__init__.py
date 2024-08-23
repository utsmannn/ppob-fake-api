from flask import Blueprint
from flask_restful import Api

from app.routes.balances import BalanceResource
from app.routes.categories import Categories
from app.routes.products import ProductResources
from app.routes.transactions import TransactionResources
from app.routes.users import UserResources

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')
api_v1 = Api(v1_bp)

api_v1.add_resource(
    ProductResources, '/product', '/product/prepaid', '/product/<int:product_id>',
    strict_slashes=False
)
api_v1.add_resource(
    Categories,
    '/category',
    strict_slashes=False
)
api_v1.add_resource(
    UserResources,
    '/user', '/user/<user_id>', '/login', '/register',
    strict_slashes=False
)
api_v1.add_resource(
    BalanceResource,
    '/topup_balance', '/topup_direct/<_id>', '/balance_invoice/<_id>', '/balance_invoice',
    strict_slashes=False
)
api_v1.add_resource(
    TransactionResources,
    '/transaction',
    '/transaction/execute',
    '/transaction/<transaction_id>',
    strict_slashes=False
)
