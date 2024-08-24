from flask import send_from_directory

from app.routes.base import BaseResources


class RootResources(BaseResources):

    def get(self):
        return send_from_directory('../site', 'home.html')