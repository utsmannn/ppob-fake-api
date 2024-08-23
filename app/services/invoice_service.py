from __future__ import annotations

import os
import uuid

from app.models import BalanceTopUpInvoice
from app.services import database
from app.services.http_client_service import HttpClientService
from app.services.user_services import user_collection, get_user

http_client = HttpClientService()
invoice_collection = database.get_collection('invoice')


def create_invoice_from_bson(invoice_bson):
    invoice = BalanceTopUpInvoice(
        _id=invoice_bson['id'],
        user_id=invoice_bson['user_id'],
        external_id=invoice_bson['external_id'],
        invoice_url=invoice_bson['invoice_url'],
        status=invoice_bson['status'],
        amount=invoice_bson['amount'],
        expired_date=invoice_bson['expired_date'],
    )

    return invoice

def url_basic_auth(url: str):
    key = os.environ.get('XENDIT_BASIC_AUTH_KEY')
    return url.replace('https://', f'https://{key}:@')


def request_invoice_balance(user, amount):
    external_id = f'{uuid.uuid4()}'.split('-')[-1]

    redirect_url = f'http://127.0.0.1:8080/api/v1/topup_direct/{external_id}'

    json_request = {
        'external_id': f'{external_id}',
        'amount': amount,
        'description': 'Balance Topup',
        'invoice_duration': 86400,
        'customer': {
            'name': user.name,
            'mobile_number': user.phone
        },
        'success_redirect_url': f'{redirect_url}',
        'failure_redirect_url': f'{redirect_url}',
        'currency': 'IDR',
        'items': [
            {
                'name': 'Saldo',
                'quantity': 1,
                'price': amount
            }
        ],
        'fees': [
            {
                'type': 'ADMIN',
                'value': 0
            }
        ],
        'metadata': {
            'store': 'Jakarta'
        }
    }

    request_invoice_url = url_basic_auth('https://api.xendit.co/v2/invoices')

    response = http_client.post(url=request_invoice_url, data=json_request)

    invoice_url = response['invoice_url']
    invoice_id = response['id']
    invoice_status = response['status']
    invoice_amount = response['amount']
    invoice_expired = response['expiry_date']

    balance_topup_invoice = BalanceTopUpInvoice(
        _id=invoice_id,
        user_id=user.id,
        external_id=external_id,
        invoice_url=invoice_url,
        status=invoice_status,
        amount=invoice_amount,
        expired_date=invoice_expired
    )

    invoice_dict = balance_topup_invoice.to_bson_dict()

    existing_invoice = invoice_collection.find_one({'id': invoice_dict['id']})
    if existing_invoice is None:
        invoice_collection.insert_one(invoice_dict)

    return balance_topup_invoice


def get_invoice(_id):
    existing_invoice = invoice_collection.find_one({'id': _id})
    if existing_invoice is None:
        return None

    return create_invoice_from_bson(existing_invoice)

def get_user_invoices(user_id):
    invoices_bson = invoice_collection.find({'user_id': user_id})

    invoices = []
    for invoice_bson in invoices_bson:
        invoice = create_invoice_from_bson(invoice_bson)
        invoices.append(invoice.to_bson_dict())

    return invoices[::-1]

def direct_update_invoice(external_id):
    existing_invoice_bson = invoice_collection.find_one({'external_id': external_id})
    if existing_invoice_bson is None:
        return None

    existing_invoice = create_invoice_from_bson(existing_invoice_bson)
    request_invoice_url = url_basic_auth(f'https://api.xendit.co/v2/invoices/{existing_invoice.id}')
    response = http_client.get(request_invoice_url)

    updated_status = response['status']
    last_update_balance = response['paid_at']

    if updated_status in ['SETTLED', 'PAID']:
        user_id = existing_invoice.user_id
        user = get_user(user_id)

        if last_update_balance != user.last_update_balance:
            current_balance = f'{user.balance}'
            amount = f'{existing_invoice.amount}'
            new_balance = int(current_balance) + int(amount)

            user_collection.update_one(
                {'id': user_id},
                {'$set': {'balance': new_balance, 'last_update_balance': last_update_balance}}, upsert=True
            )

        new_status = 'PAID'
    else:
        new_status = updated_status

    invoice_collection.update_one({'external_id': external_id}, {'$set': {'status': new_status}}, upsert=True)
