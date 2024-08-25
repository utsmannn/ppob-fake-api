from flask import send_from_directory

from src.routes.base import BaseResources


class DocumentationResources(BaseResources):

    def get(self, file=None):
        print(f'asuuuuuuuu ciuu -> {self.base_path}')
        if file is None:
            return send_from_directory('../site', 'index.html')
        elif self.base_path == '/payment-simulation/':
            directory_target = self.base_path.rsplit('/', 1)[0]
            return send_from_directory(f'../site', f'{directory_target}index.html')
        else:
            directory_target = self.base_path.rsplit('/', 1)[0]
            return send_from_directory(f'../site{directory_target}', file)
