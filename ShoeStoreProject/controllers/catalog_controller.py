from flask import Blueprint, render_template, request
from services.catalog_service import catalog_service

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/catalog')
def catalog():
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')

    if search_term:
        products = catalog_service.search_products(search_term)
    else:
        products = catalog_service.products

    reverse = (sort_order == 'desc')
    if sort_by in ['name', 'price', 'stock']:
        products = catalog_service.sort_products(sort_by, reverse)

    return render_template('catalog.html',
                           products=products,
                           search_term=search_term,
                           sort_by=sort_by,
                           sort_order=sort_order)


@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        return "Продуктът не е намерен", 404

    return render_template('product_detail.html', product=product)