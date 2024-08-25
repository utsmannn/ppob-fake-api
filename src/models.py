__all__ = ['ProductRawCsv', 'User', 'BalanceTopUpInvoice', 'Transaction', 'PrepaidAccountTransaction']


class ProductRawCsv:
    def __init__(self, _id, code, name, category, sub_category, description, nominal_min, nominal_max, admin_fee,
                 service_fee, status):
        self._id = _id
        self.code = code
        self.name = name
        self.category = category
        self.sub_category = sub_category
        self.description = description
        self.nominal_min = nominal_min
        self.nominal_max = nominal_max
        self.admin_fee = admin_fee
        self.service_fee = service_fee
        self.status = status

    def __repr__(self):
        return f"<Product {self.code}: {self.name}>"

    def to_dict(self):
        return {
            "id": self._id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "sub_category": self.sub_category,
            "description": self.description,
            "nominal": None if self.nominal_min != self.nominal_max else self.nominal_min,
            "admin_fee": self.admin_fee,
            "service_fee": self.service_fee,
            "status": self.status
        }


class User:
    def __init__(self, _id, name, phone, password, balance, last_update_balance):
        self._id = _id
        self.name = name
        self.phone = phone
        self.password = password
        self.balance = balance
        self.last_update_balance = last_update_balance

    def __repr__(self):
        return f"<User {self.name}: {self.phone}>"

    @property
    def id(self):
        return self._id

    def to_dict_without_password(self):
        return {
            'id': self._id,
            'name': self.name,
            'phone': self.phone,
            'balance': self.balance,
            'last_update_balance': self.last_update_balance
        }

    def to_bson_dict(self):
        return {
            'id': self._id,
            'name': self.name,
            'phone': self.phone,
            'password': self.password,
            'balance': self.balance,
            'last_update_balance': self.last_update_balance
        }


class BalanceTopUpInvoice:
    def __init__(self, _id, user_id, external_id, invoice_url, status, amount, expired_date):
        self._id = _id
        self.user_id = user_id
        self.external_id = external_id
        self.invoice_url = invoice_url
        self.status = status
        self.amount = amount
        self.expired_date = expired_date

    @property
    def id(self):
        return self._id

    def to_bson_dict(self):
        return {
            'id': self._id,
            'user_id': self.user_id,
            'external_id': self.external_id,
            'invoice_url': self.invoice_url,
            'status': self.status,
            'amount': self.amount,
            'expired_date': self.expired_date
        }


class PrepaidAccountTransaction:
    def __init__(self, prepaid_account_name, prepaid_account_number):
        self.prepaid_account_name = prepaid_account_name
        self.prepaid_account_number = prepaid_account_number

    def to_bson_dict(self):
        return {
            'name': self.prepaid_account_name,
            'number': self.prepaid_account_number
        }


class Transaction:
    def __init__(self, _id, product_code, user_id, amount, date, status, recipient_number,
                 prepaid_account: PrepaidAccountTransaction, description):
        self._id = _id
        self.product_code = product_code
        self.user_id = user_id
        self.amount = amount
        self.date = date
        self.status = status
        self.recipient_number = recipient_number
        self.prepaid_account = prepaid_account
        self.description = description

    @property
    def id(self):
        return self._id

    def to_bson_dict(self):

        return {
            'id': self._id,
            'product_code': self.product_code,
            'user_id': self.user_id,
            'amount': self.amount,
            'date': self.date,
            'status': self.status,
            'recipient_number': self.recipient_number,
            'prepaid_account': None if self.prepaid_account is None else self.prepaid_account.to_bson_dict(),
            'description': self.description
        }