from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import auth_service
from services.catalog_service import catalog_service
from services.order_service import order_service

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Моля, влезте в акаунта си.', 'warning')
            return redirect(url_for('auth.login'))

        user = auth_service.get_user_by_id(session['user_id'])
        if not user or not user.is_admin:
            flash('Нямате права за достъп до тази страница.', 'error')
            return redirect(url_for('index'))

        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return redirect(url_for('admin.products'))


@admin_bp.route('/products')
@admin_required
def products():
    products = catalog_service.products
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        color = request.form['color']
        sizes = [int(s.strip()) for s in request.form['sizes'].split(',')]
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        product = catalog_service.add_product(name, description, color, sizes, price, stock)
        flash(f'Продукт "{name}" е добавен успешно!', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/edit_product.html')


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash('Продуктът не е намерен.', 'error')
        return redirect(url_for('admin.products'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        color = request.form['color']
        sizes = [int(s.strip()) for s in request.form['sizes'].split(',')]
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        success = catalog_service.update_product(product_id,
                                                 name=name,
                                                 description=description,
                                                 color=color,
                                                 sizes=sizes,
                                                 price=price,
                                                 stock=stock)

        if success:
            flash(f'Продукт "{name}" е обновен успешно!', 'success')
        else:
            flash('Грешка при обновяване на продукта.', 'error')

        return redirect(url_for('admin.products'))

    return render_template('admin/edit_product.html', product=product)


@admin_bp.route('/products/delete/<int:product_id>')
@admin_required
def delete_product(product_id):
    success = catalog_service.delete_product(product_id)
    if success:
        flash('Продуктът е изтрит успешно!', 'success')
    else:
        flash('Грешка при изтриване на продукта.', 'error')

    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
@admin_required
def view_orders():
    orders = order_service.get_all_orders()
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/update_status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    new_status = request.form['status']
    success = order_service.update_order_status(order_id, new_status)

    if success:
        flash(f'Статусът на поръчка #{order_id} е обновен на "{new_status}"', 'success')
    else:
        flash('Грешка при обновяване на статуса.', 'error')

    return redirect(url_for('admin.view_orders'))