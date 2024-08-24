from flask import send_from_directory

from app.routes.base import BaseResources


class DocumentationResources(BaseResources):

    def get(self, file=None):
        if file is None:
            return send_from_directory('../site', 'index.html')
        else:
            path_file = self.base_path.replace('/assets', 'assets')
            return send_from_directory('../site', path_file)