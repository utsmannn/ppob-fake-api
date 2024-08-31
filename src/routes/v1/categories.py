from src.routes.base import BaseResources


class Categories(BaseResources):

    def get(self):

        data = [cat.to_dict() for cat in self.categories]
        return self.create_response(
            message='Get category success',
            status=True,
            data=data
        )