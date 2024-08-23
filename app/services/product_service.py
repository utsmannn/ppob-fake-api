import csv
from typing import Dict

from app.models import ProductRawCsv

def load_products():
    products = []
    with open('products.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader, start=1):
            row: Dict[str, str]
            product = ProductRawCsv(
                _id=index,
                code=row['code'],
                name=row['name'],
                category=row['category'],
                sub_category=row['subcategory'],
                description=row['description'],
                nominal_min=float(row['nominal_min']),
                nominal_max=float(row['nominal_max']),
                admin_fee=float(row['admin_fee']),
                service_fee=float(row['service_fee']),
                status=row['status']
            )
            products.append(product)
    return products