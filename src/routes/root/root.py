from dataclasses import asdict
from lib2to3.fixes.fix_input import context

from flask import request

from src.routes.base import BaseResources
from src.services.qris_service import parse_qris


class RootResources(BaseResources):

    def get(self):
        content = request.args.get('content', default=None, type=str)
        if content is None:
            return self.abort_response(
                code=500,
                message='query content not found'
            )

        qris_data = parse_qris(content)
        if qris_data:
            return self.create_response(
                message='ok',
                status=True,
                data=asdict(qris_data)
            )
        else:
            self.abort_response(
                code=500,
                message='QRIS invalid'
            )