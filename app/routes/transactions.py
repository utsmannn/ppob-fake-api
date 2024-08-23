from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.routes.base import BaseResources
from app.services.transaction_service import inquiry_transaction, get_transaction, get_all_transaction, \
    execute_transaction
from app.services.user_services import get_user, get_user_with_password


class TransactionResources(BaseResources):

    @jwt_required()
    def post(self):
        path = self.base_path
        user_id = get_jwt_identity()

        if path == '/transaction':
            return self.inquiry_transaction(user_id)
        elif path == '/transaction/execute':
            return self.execute_transaction(user_id)
        else:
            self.abort_response(404, 'Invalid route')

    def inquiry_transaction(self, user_id):
        data = request.json
        if data is None:
            self.abort_response(500, 'Body empty!')

        required_fields = ['product_code', 'recipient_number']
        for field in required_fields:
            if field not in data:
                return self.abort_response(400, f'Missing field: {field}')

        product_code = data['product_code']
        recipient_number = data['recipient_number']
        user = get_user(user_id)

        transaction = inquiry_transaction(product_code, user, recipient_number)

        if transaction is None:
            self.abort_response(404, 'Product not found')

        return self.create_response(
            message='Transaction created successful',
            status=True,
            data=transaction.to_bson_dict()
        )

    def execute_transaction(self, user_id):
        data = request.json
        if data is None:
            self.abort_response(500, 'Body empty!')

        required_fields = ['transaction_id', 'password']
        for field in required_fields:
            if field not in data:
                return self.abort_response(400, f'Missing field: {field}')

        transaction_id = data['transaction_id']
        password = data['password']
        user = get_user_with_password(user_id)

        transaction_result = execute_transaction(transaction_id, user, password)

        status = transaction_result['status']
        message = transaction_result['message']
        if not status:
            self.abort_response(500, message)

        transaction_bson = transaction_result['transaction']
        return self.create_response(
            message=message,
            status=True,
            data=transaction_bson
        )

    @jwt_required()
    def get(self, transaction_id=None):
        if transaction_id is None:
            return self.get_all_transaction()
        else:
            return self.get_transaction_by_id(transaction_id)

    def get_transaction_by_id(self, transaction_id):
        transaction = get_transaction(transaction_id)
        if transaction is None:
            self.abort_response(404, 'Transaction not found!')

        return self.create_response(
            message='get Transaction success',
            status=True,
            data=transaction.to_bson_dict()
        )

    def get_all_transaction(self):
        user_id = get_jwt_identity()
        transactions = get_all_transaction(user_id)

        return self.create_response(
            message='get Transactions success',
            status=True,
            data=transactions
        )
