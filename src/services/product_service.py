import csv
from typing import Dict
from unicodedata import category

from src.models import ProductRawCsv, CategoryRawCsv


def load_products():
    products = []
    with open('products.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader, start=1):
            row: Dict[str, str]
            icon_name = row['icon_name']
            icon = f'https://utsmannn.github.io/images/{icon_name}'
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
                status=row['status'],
                icon=icon
            )
            products.append(product)
    return products


def load_categories():
    categories = []
    with open('categories.csv', mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader, start=1):
            row: Dict[str, str]
            icon_name = row['icon_name']
            icon = f'https://utsmannn.github.io/images/{icon_name}'

            subcategories_raw = row['subcategory']
            subcategories = subcategories_raw.split('|')

            prod_category = CategoryRawCsv(
                name=row['category'],
                subcategories=subcategories,
                icon=icon
            )

            categories.append(prod_category)
    return categories