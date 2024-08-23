from unicodedata import category

from flask import request, jsonify
from flask_restful import Resource, abort

from app.services.product_service import load_products


class BaseResources(Resource):

    def __init__(self):
        self._categories_raw = {}

        self.all_product = load_products()
        self.base_path = request.path.replace('/api/v1', '')

        for prd in self.all_product:
            if prd.category not in self._categories_raw:
                self._categories_raw[prd.category] = []
            if prd.sub_category not in self._categories_raw[prd.category]:
                self._categories_raw[prd.category].append(prd.sub_category)

        self.categories = [
            {
                'category': category_name,
                'sub_category': sub_categories_name
            }
            for category_name, sub_categories_name in self._categories_raw.items()
        ]

    def category_arg(self):
        return request.args.get('category', default=None, type=str)

    def search_arg(self):
        return request.args.get('search', default=None, type=str)

    def create_response(self, message, status, data=None):
        response = {
            'message': message,
            'status': status
        }

        if data is not None:
            response['data'] = data

        return jsonify(response)

    def abort_response(self, code, message):
        abort(code, message=message, status=False)