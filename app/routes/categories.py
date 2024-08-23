from app.routes.base import BaseResources


class Categories(BaseResources):

    def get(self):
        return self.create_response(
            message='Get category success',
            status=True,
            data=self.categories
        )