from faker import Faker
from static import PRODUCTS
from random import choice

fake = Faker()


def fake_customer():
    fake: Faker = Faker(['ru_RU'])
    person = fake.simple_profile()
    return {'name': person['name'],
            'phone': fake.phone_number(),
            'email': person['mail']}


def fake_product() -> tuple:
    rand_product = choice(PRODUCTS)

    product = {
        "name": rand_product["name"],
        "description": rand_product["description"],
        "price": rand_product["price"]
    }

    product_photo_url = rand_product["photo_url"]
    return product, product_photo_url


def generate_products():
    return [{"name": product["name"],
             "description": product["description"],
             "price": product["price"],
             "photo_url": product["photo_url"]} for product in PRODUCTS]
