from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.cart_service import cart_service
from services.catalog_service import catalog_service
from services.order_service import order_service
from services.notification_service import notification_service
from services.auth_service import auth_service


cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
def view_cart():
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си за да видите кошницата.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = cart_service.get_cart(user_id)

    cart_with_details = []
    for item in cart_items:
        product = catalog_service.get_product_by_id(item.product_id)
        if product:
            cart_with_details.append({
                'product': product,
                'size': item.size,
                'quantity': item.quantity,
                'subtotal': product.price * item.quantity
            })

    total = cart_service.get_cart_total(user_id, catalog_service)

    return render_template('cart.html',
                           cart_items=cart_with_details,
                           total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    size = request.form.get('size')
    quantity = int(request.form.get('quantity', 1))

    product = catalog_service.get_product_by_id(product_id)
    if not product:
        flash('Продуктът не е намерен.', 'error')
        return redirect(url_for('catalog.catalog'))

    if size not in product.sizes:
        flash('Невалиден размер.', 'error')
        return redirect(url_for('catalog.product_detail', product_id=product_id))

    if quantity > product.stock:
        flash('Недостатъчна наличност.', 'error')
        return redirect(url_for('catalog.product_detail', product_id=product_id))

    cart_service.add_to_cart(user_id, product_id, size, quantity)
    flash('Продуктът е добавен в кошницата!', 'success')
    return redirect(url_for('catalog.product_detail', product_id=product_id))


@cart_bp.route('/cart/remove/<int:product_id>/<size>')
def remove_from_cart(product_id, size):
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_service.remove_from_cart(user_id, product_id, size)
    flash('Продуктът е премахнат от кошницата.', 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/update/<int:product_id>/<size>', methods=['POST'])
def update_cart_quantity(product_id, size):
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    quantity = int(request.form.get('quantity', 1))

    product = catalog_service.get_product_by_id(product_id)
    if quantity > product.stock:
        flash('Недостатъчна наличност.', 'error')
        return redirect(url_for('cart.view_cart'))

    cart_service.update_quantity(user_id, product_id, size, quantity)
    flash('Количеството е обновено.', 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си за да направите поръчка.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = cart_service.get_cart(user_id)

    if not cart_items:
        flash('Кошницата ви е празна.', 'warning')
        return redirect(url_for('cart.view_cart'))

    if request.method == 'POST':
        address = request.form['address']
        payment_method = request.form['payment_method']

        order = order_service.create_order(user_id, cart_items, address, payment_method, catalog_service)

        if order:
            cart_service.clear_cart(user_id)
            user = auth_service.get_user_by_id(user_id)
            notification_service.notify(user, "order", order)

            flash(f'Поръчката ви е направена успешно! Номер на поръчка: #{order.id}', 'success')
            return redirect(url_for('cart.view_orders'))
        else:
            flash('Грешка при създаване на поръчката. Моля, опитайте отново.', 'error')

    total = cart_service.get_cart_total(user_id, catalog_service)
    return render_template('checkout.html', total=total)


@cart_bp.route('/orders')
def view_orders():
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си за да видите поръчките си.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    orders = order_service.get_orders_by_user(user_id)

    return render_template('orders.html', orders=orders)


@cart_bp.route('/notifications')
def view_notifications():
    if 'user_id' not in session:
        flash('Моля, влезте в акаунта си.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    notifications = notification_service.get_user_notifications(user_id)

    return render_template('notifications.html', notifications=notifications)


@cart_bp.route('/notifications/mark_read/<int:notification_id>')
def mark_notification_read(notification_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    notification_service.mark_as_read(notification_id, user_id)
    flash('Нотификацията е маркирана като прочетена.', 'success')
    return redirect(url_for('cart.view_notifications'))


@cart_bp.route('/notifications/mark_all_read')
def mark_all_notifications_read():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    notification_service.mark_all_as_read(user_id)
    flash('Всички нотификации са маркирани като прочетени.', 'success')
    return redirect(url_for('cart.view_notifications'))