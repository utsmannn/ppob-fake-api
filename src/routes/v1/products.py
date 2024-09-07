from unicodedata import category

from src.routes.base import BaseResources


class ProductResources(BaseResources):

    def get(self, product_code=None):
        if product_code is not None:
            return self.get_by_code(product_code)
        elif self.base_path == '/product/prepaid':
            return self.get_all_pre_paid()
        else:
            return self.get_all_post_paid()

    def get_all_post_paid(self):
        all_products = (prd for prd in self.all_product if prd.nominal_max == prd.nominal_min)
        if self.category_arg():
            products = (prd for prd in all_products if prd.category.lower() == self.category_arg().lower())
            if self.subcategory_arg():
                products = (prd for prd in products if self.subcategory_arg().lower() in prd.sub_category.lower())
        elif self.search_arg():
            products = (prd for prd in all_products if self.search_arg().lower() in prd.name.lower())
        else:
            products = all_products

        data = [prd.to_dict() for prd in products]

        if not data:
            self.abort_response(404, 'Product not found')
        else:
            return self.create_response(
                message='Get products success',
                status=True,
                data=data
            )

    def get_all_pre_paid(self):
        all_products = (prd for prd in self.all_product if prd.nominal_max != prd.nominal_min)
        if self.category_arg():
            products = (prd for prd in all_products if prd.category.lower() == self.category_arg().lower())
        elif self.search_arg():
            products = (prd for prd in all_products if self.search_arg().lower() in prd.name.lower())
        else:
            products = (prd for prd in self.all_product if prd.nominal_max != prd.nominal_min)

        data = [prd.to_dict() for prd in products]

        if not data:
            self.abort_response(404, 'Product not found')
        else:
            return self.create_response(
                message='Get products success',
                status=True,
                data=data
            )

    def get_by_id(self, product_id):
        prd = next((prd for prd in self.all_product if prd.id == product_id), None)
        if prd:
            return self.create_response(
                message=f'Product with id: {product_id} found!',
                status=True,
                data=prd.to_dict()
            )
        else:
            self.abort_response(404, f'Product with id: {product_id} not found!')

    def get_by_code(self, code):
        prd = next((prd for prd in self.all_product if prd.code == code), None)
        if prd:
            return self.create_response(
                message=f'Product with code: {code} found!',
                status=True,
                data=prd.to_dict()
            )
        else:
            self.abort_response(404, f'Product with code: {code} not found!')
