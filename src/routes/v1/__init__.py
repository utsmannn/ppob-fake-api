from flask import Blueprint, url_for
from flask_restful import Api
from werkzeug.utils import redirect

from src.routes.v1.balances import BalanceResource
from src.routes.v1.categories import Categories
from src.routes.v1.documentations import DocumentationResources
from src.routes.v1.products import ProductResources
from src.routes.v1.transactions import TransactionResources
from src.routes.v1.users import UserResources

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')
api_v1 = Api(v1_bp)

@api_v1.app.route('/')
def root_v1():
    return redirect(url_for('root.rootresources'))

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
    '/transaction/qris',
    '/transaction/<transaction_id>',
    strict_slashes=False
)
api_v1.add_resource(
    DocumentationResources,
    '/docs',
    '/assets/stylesheets/<file>',
    '/assets/javascripts/<file>',
    '/assets/images/<file>',
    '/assets/javascripts/workers/<file>',
    '/search/<file>',
    '/docs/#<file>'
)


def sample_register():
    """
    :rtype: object
    """
    return {}