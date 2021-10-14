from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound, BadRequest

products_bp = Blueprint('products', __name__)

PRODUCTS_DATA = {
    1: {'goods': 'macbook air m1', 
        'description': '13.3 Ноутбук Apple MacBook Air 13 Late 2020 (2560x1600, Apple M1 3.2 ГГц, RAM 16 ГБ, SSD 512 ГБ, Apple graphics 8-core), Z12B00048, золотой', 
        'price': 135.470
        },
    2: {'goods': 'iphone xr', 
        'description': 'Apple iPhone XR 128Gb Yellow (Жёлтый)', 
        'price': 43.990
        },
    3: {'goods': 'apple watch se', 
        'description': 'Умные часы Apple Watch SE GPS 40мм Aluminum Case with Sport Band, серый космос/тёмная ночь', 
        'price': 24.710
        },
}

@products_bp.route('/', endpoint='products_list')
def products_list_view():
    return render_template("products/list.html", products=PRODUCTS_DATA)

# CRUD
@products_bp.route('/create/', methods=('GET', 'POST'), endpoint='product_create')
def products_create_view():
    if request.method == "GET":
        return render_template("products/create.html")

    goods = request.form.get("product-goods")
    description = request.form.get("product-description")
    price = request.form.get("product-price")
    if not goods:
        raise BadRequest("Please provide product name!")

    product_id = len(PRODUCTS_DATA) + 1
    new_product = {
                product_id : {
                    'goods': goods,
                    'description': description,
                    'price': price
                }
                }
    PRODUCTS_DATA.update(new_product)
    return redirect(url_for("products.product_detail", product_id=product_id))

@products_bp.route('/<int:product_id>', endpoint='product_detail')
def products_read_view(product_id: int):
    product = PRODUCTS_DATA.get(product_id)
    if product is None:
        raise NotFound(f"No product for id {product_id}")
    return render_template("products/detail.html", 
    product_id=product_id, 
    product=product)

@products_bp.route('/<int:product_id>', endpoint='product_update')
def products_update_view(product_id: int):
    pass

@products_bp.route('/<int:product_id>', endpoint='product_delete')
def products_delete_view():
    pass
