from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import abort

from app.routes.base import BaseResources
from app.services.user_services import register, get_user_dict, login


class UserResources(BaseResources):

    def post(self):
        if self.base_path == '/register':
            return self.register()
        elif self.base_path == '/login':
            return self.login()
        else:
            abort(404)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = get_user_dict(user_id)
        return self.create_response(
            message='Get user success',
            status=True,
            data=user
        )

    def register(self):
        data = request.json
        required_fields = ['name', 'phone', 'password']
        for field in required_fields:
            if field not in data:
                return self.abort_response(400, f'Missing field: {field}')

        name = data['name']
        phone = data['phone']
        password = data['password']

        register_result = register(name, phone, password)
        if register_result:
            return self.create_response(
                message='User success register',
                status=True,
                data=register_result
            )
        else:
            self.abort_response(401, f'Already user registered with phone: {phone}')

    def login(self):
        phone = request.json['phone']
        password = request.json['password']

        login_result = login(phone, password)

        status = login_result['status']
        message = login_result['message']

        if status:
            token = login_result['token']
            return self.create_response(
                message=message,
                data=token,
                status=True
            )
        else:
            self.abort_response(
                code=401,
                message=message
            )
