
from flask import request, make_response, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.routes.base import BaseResources
from app.services.user_services import get_user
from app.services.invoice_service import request_invoice_balance, direct_update_invoice, get_invoice, get_user_invoices


class BalanceResource(BaseResources):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = request.json

        if data is None:
            self.abort_response(500, 'Body empty!')

        required_fields = ['amount']
        for field in required_fields:
            if field not in data:
                return self.abort_response(400, f'Missing field: {field}')

        amount = data['amount']
        user = get_user(user_id)
        invoice = request_invoice_balance(user, amount).to_bson_dict()
        return self.create_response(
            message='Create request invoice for topup balance success',
            status=True,
            data=invoice
        )

    def get(self, _id=None):
        path = self.base_path

        if path == f'/topup_direct/{_id}':
            return self.get_redirect(_id)

        elif path == f'/balance_invoice/{_id}':
            return self.get_topup_id(_id)

        elif path == '/balance_invoice':
            return self.get_topup()

        else:
            abort(404, description="Resource not found")

    @jwt_required()
    def get_topup(self):
        user_id = get_jwt_identity()
        invoices = get_user_invoices(user_id)

        return self.create_response(
            message='Get invoice success',
            status=True,
            data=invoices
        )

    def get_redirect(self, external_id):
        direct_update_invoice(external_id)
        html_content = """
                    <html>
                        <head><title>Invoice Paid!</title></head>
                        <body>
                            <p>Thank you for your payment.</p>
                        </body>
                    </html>
                    """
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response

    @jwt_required()
    def get_topup_id(self, _id):
        invoice = get_invoice(_id)
        if invoice is None:
            self.abort_response(404, message='Invoice not found!')

        return self.create_response(
            message='Invoice found',
            status=True,
            data=invoice.to_bson_dict()
        )
