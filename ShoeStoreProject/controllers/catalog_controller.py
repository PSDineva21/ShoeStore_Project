from flask import Blueprint, render_template, request

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/catalog')
def catalog():
    from services.catalog_service import catalog_service

    search_term = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    gender = request.args.get('gender', '')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')


    products = catalog_service.products


    if search_term:
        products = catalog_service.search_products(search_term)
        print(f"DEBUG: Търсене за '{search_term}' - намерени {len(products)} продукта")

    if category:
        products = [p for p in products if p.category == category]
        print(f"DEBUG: Филтриране по категория '{category}' - останали {len(products)} продукта")

    if gender:
        products = [p for p in products if p.gender == gender or p.gender == 'unisex']
        print(f"DEBUG: Филтриране по пол '{gender}' - останали {len(products)} продукта")


    reverse = (sort_order == 'desc')
    if sort_by in ['name', 'price', 'stock']:
        products = catalog_service.sort_products(products, sort_by, reverse)

    return render_template('catalog.html',
                           products=products,
                           search_term=search_term,
                           category=category,
                           gender=gender,
                           sort_by=sort_by,
                           sort_order=sort_order,
                           catalog_service=catalog_service)

@catalog_bp.route('/category/<category_name>')
def category_view(category_name):
    from services.catalog_service import catalog_service

    gender = request.args.get('gender', '')

    if gender:
        products = catalog_service.get_products_by_category_and_gender(category_name, gender)
    else:
        products = catalog_service.get_products_by_category(category_name)

    return render_template('category.html',
                         products=products,
                         category=category_name,
                         gender=gender,
                         catalog_service=catalog_service)

@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    from services.catalog_service import catalog_service

    product = catalog_service.get_product_by_id(product_id)
    if not product:
        return "Продуктът не е намерен", 404

    return render_template('product_detail.html', product=product)