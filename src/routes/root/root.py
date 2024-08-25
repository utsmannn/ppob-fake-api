from flask import send_from_directory
from werkzeug.utils import redirect

from src.routes.base import BaseResources


class RootResources(BaseResources):

    def get(self):
        return redirect('https://utsmannn.github.io/ppob-fake-api')