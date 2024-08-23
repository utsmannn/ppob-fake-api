import uuid
from datetime import timedelta

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.services import database

user_collection = database.get_collection('user')

def register(name, phone, password):
    existing_by_phone = user_collection.find_one({'phone': phone})
    hashed_password = generate_password_hash(password, method='pbkdf2')

    if not existing_by_phone:
        user_id = f'{uuid.uuid4()}'.split('-')[-1]
        user = User(user_id, name, phone, hashed_password, 0, None).to_bson_dict()
        user_collection.insert_one(user)
        return 'Register successful, please login'
    else:
        return None

def login(phone, password):
    existing_user_by_phone = user_collection.find_one({'phone': phone})
    if existing_user_by_phone is None:
        return {
            'status': False,
            'message': f'User with {phone} not found'
        }

    hashed_password = existing_user_by_phone['password']

    is_password_valid = check_password_hash(hashed_password, password)
    user_id = create_user_dict_from_bson(existing_user_by_phone).get('id')

    expires_delta = timedelta(days=1)
    token = create_access_token(identity=f'{user_id}', expires_delta=expires_delta)

    if is_password_valid:
        return {
            'status': True,
            'token': token,
            'message': f'User with {phone} has found'
        }
    else:
        return {
            'status': False,
            'message': f'User with {phone} wrong password'
        }


def create_user_dict_from_bson(user_bson):
    user = User(
        _id=user_bson['id'],
        name=user_bson['name'],
        phone=user_bson['phone'],
        password=user_bson['password'],
        balance=user_bson['balance'],
        last_update_balance = user_bson['last_update_balance']
    ).to_dict_without_password()

    return user

def create_user_with_password_dict_from_bson(user_bson):
    user = User(
        _id=user_bson['id'],
        name=user_bson['name'],
        phone=user_bson['phone'],
        password=user_bson['password'],
        balance=user_bson['balance'],
        last_update_balance = user_bson['last_update_balance']
    ).to_bson_dict()

    return user

def create_user_from_dict(user_dict) -> User:
    if 'password' not in user_dict:
        password = None
    else:
        password = user_dict['password']

    return User(
        _id=user_dict['id'],
        name=user_dict['name'],
        phone=user_dict['phone'],
        password=password,
        balance=user_dict['balance'],
        last_update_balance=user_dict['last_update_balance']
    )

def get_user_dict(_id):
    user_bson = user_collection.find_one({'id': _id})
    user = create_user_dict_from_bson(user_bson)
    return user

def get_user(_id):
    user_bson = user_collection.find_one({'id': _id})
    user_dict = create_user_dict_from_bson(user_bson)
    user = create_user_from_dict(user_dict)
    return user

def get_user_with_password(_id):
    user_bson = user_collection.find_one({'id': _id})
    user_dict = create_user_with_password_dict_from_bson(user_bson)
    user = create_user_from_dict(user_dict)
    return user