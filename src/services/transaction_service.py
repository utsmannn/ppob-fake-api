import random
import uuid
from datetime import datetime

from werkzeug.security import check_password_hash

from src.models import User, PrepaidAccountTransaction, Transaction, MerchantAccount
from src.services import database
from src.services.product_service import load_products
from src.services.qris_service import parse_qris, QrisData
from src.services.user_services import user_collection

transaction_collection = database.get_collection('transaction')


def format_rupiah(value):
    rupiah_format = f"Rp{value:,.0f}".replace(",", ".")
    return rupiah_format


def create_transaction_from_bson(bson_transaction):
    if 'prepaid_account' in bson_transaction:
        prepaid_account_bson = bson_transaction['prepaid_account']
        if prepaid_account_bson is None:
            prepaid_account = None
        else:
            prepaid_account = PrepaidAccountTransaction(
                prepaid_account_name=prepaid_account_bson['name'],
                prepaid_account_number=prepaid_account_bson['number']
            )
    else:
        prepaid_account = None

    if 'merchant_account' in bson_transaction:
        merchant_account_bson = bson_transaction['merchant_account']
        if merchant_account_bson is None:
            merchant_account = None
        else:
            merchant_account = MerchantAccount(
                name=merchant_account_bson['name'],
                city=merchant_account_bson['city'],
                merchant_id=merchant_account_bson['id']
            )
    else:
        merchant_account = None

    transaction = Transaction(
        _id=bson_transaction['id'],
        product_code=bson_transaction['product_code'],
        user_id=bson_transaction['user_id'],
        amount=bson_transaction['amount'],
        date=bson_transaction['date'],
        status=bson_transaction['status'],
        recipient_number=bson_transaction['recipient_number'],
        prepaid_account=prepaid_account,
        merchant_account=merchant_account,
        description=bson_transaction['description']
    )
    return transaction


def inquiry_transaction(product_code, user: User, recipient_number):
    products = load_products()

    product = next((product for product in products if product.code == product_code), None)
    if product is None:
        return None

    is_postpaid = product.nominal_min == product.nominal_max

    fee = product.admin_fee + product.service_fee

    if is_postpaid:
        _recipient_number = recipient_number
        amount = float(f'{product.nominal_min}') + fee
        description = product.description
        prepaid_account = None
    else:
        _recipient_number = None
        int_nominal_min = int(float(f'{product.nominal_min}'))
        int_nominal_max = int(float(f'{product.nominal_max}'))
        amount = random.randint(int_nominal_min, int_nominal_max) + fee
        account_name = 'Fulan bin Fulan'
        description = product.description + f' {account_name}' + f' {format_rupiah(amount)}'
        prepaid_account = PrepaidAccountTransaction(
            prepaid_account_name=account_name,
            prepaid_account_number=recipient_number
        )

    date_now = datetime.utcnow()
    date_formatted = date_now.isoformat(timespec='milliseconds') + 'Z'

    transaction_id = f'{uuid.uuid4()}'.split('-')[-1]
    if float(f'{user.balance}') > float(f'{amount}'):
        status = 'PENDING'
    else:
        status = 'FAILED'

    transaction = Transaction(
        _id=transaction_id,
        product_code=product_code,
        user_id=user.id,
        amount=int(amount),
        date=date_formatted,
        status=status,
        recipient_number=_recipient_number,
        prepaid_account=prepaid_account,
        merchant_account=None,
        description=description
    )

    transaction_collection.insert_one(transaction.to_bson_dict())

    if status == 'SUCCESS':
        updated_balance = int(float(user.balance)) - int(float(amount))
        user_collection.update_one(
            {'id': user.id}, {'$set': {'balance': updated_balance}},
            upsert=True
        )

    return transaction

def inquiry_qris_transaction(qris_data: QrisData, user: User, external_amount):
    merchant_id = qris_data.merchant_account_2.merchant_id
    merchant_account = MerchantAccount(
        name=qris_data.merchant_name,
        city=qris_data.merchant_city,
        merchant_id=merchant_id
    )

    date_now = datetime.utcnow()
    date_formatted = date_now.isoformat(timespec='milliseconds') + 'Z'
    amount = float(f'{external_amount}')

    transaction_id = f'{uuid.uuid4()}'.split('-')[-1]
    if float(f'{user.balance}') > float(f'{amount}'):
        status = 'PENDING'
    else:
        status = 'FAILED'

    description = f'{qris_data.merchant_name}, {qris_data.merchant_city}'

    transaction = Transaction(
        _id=transaction_id,
        product_code='QRIS',
        user_id=user.id,
        amount=int(amount),
        date=date_formatted,
        status=status,
        recipient_number=None,
        prepaid_account=None,
        description=description,
        merchant_account=merchant_account
    )

    transaction_collection.insert_one(transaction.to_bson_dict())

    if status == 'SUCCESS':
        updated_balance = int(float(user.balance)) - int(float(amount))
        user_collection.update_one(
            {'id': user.id}, {'$set': {'balance': updated_balance}},
            upsert=True
        )

    return transaction


def execute_transaction(transaction_id, user: User, password):
    transaction = get_transaction(transaction_id)
    status = transaction.status
    amount = transaction.amount

    hashed_password = user.password
    is_password_valid = check_password_hash(hashed_password, password)

    if not is_password_valid:
        return {
            'status': False,
            'message': 'Invalid password'
        }

    if status == 'PENDING':
        transaction_collection.update_one(
            {'id': transaction_id},
            {'$set': {'status': 'SUCCESS'}},
            upsert=True
        )

        updated_balance = int(float(user.balance)) - int(float(amount))
        user_collection.update_one(
            {'id': user.id}, {'$set': {'balance': updated_balance}},
            upsert=True
        )
    else:
        return {
            'status': False,
            'message': f'Cannot execute transaction with status {status}'
        }

    updated_transaction_bson = transaction_collection.find_one(
        {'id': transaction_id}
    )
    updated_transaction = create_transaction_from_bson(updated_transaction_bson)

    return {
        'status': True,
        'message': 'Successful execute transaction',
        'transaction': updated_transaction.to_bson_dict()
    }


def get_transaction(transaction_id):
    transaction_bson = transaction_collection.find_one({'id': transaction_id})
    if transaction_bson is None:
        return None

    transaction = create_transaction_from_bson(transaction_bson)
    return transaction


def get_all_transaction(user_id):
    transactions_bson = transaction_collection.find({'user_id': user_id})

    transactions = []
    for transaction_bson in transactions_bson:
        transaction = create_transaction_from_bson(transaction_bson)
        transactions.append(transaction.to_bson_dict())

    return transactions[::-1]
