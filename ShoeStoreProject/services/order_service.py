from datetime import datetime


class OrderItem:


    def __init__(self, product_id, size, quantity, price):
        self._product_id = product_id
        self._size = size
        self._quantity = quantity
        self._price = price

    @property
    def product_id(self):
        return self._product_id

    @property
    def size(self):
        return self._size

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def subtotal(self):
        return self._price * self._quantity


class Order:


    def __init__(self, id, user_id, items, address, payment_method):
        self._id = id
        self._user_id = user_id
        self._items = items
        self._address = address
        self._payment_method = payment_method
        self._created_at = datetime.now()
        self._status = "Обработва се"

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def items(self):
        return self._items.copy()

    @property
    def address(self):
        return self._address

    @property
    def payment_method(self):
        return self._payment_method

    @property
    def created_at(self):
        return self._created_at

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ["Обработва се", "Потвърдена", "Изпратена", "Доставена", "Отказана"]
        if value in valid_statuses:
            self._status = value
        else:
            raise ValueError("Невалиден статус на поръчка")

    @property
    def total(self):
        return sum(item.subtotal for item in self._items)


class OrderService:


    def __init__(self):
        self._orders = []
        self._next_id = 1

    def create_order(self, user_id, cart_items, address, payment_method, catalog_service):
        order_items = []
        for cart_item in cart_items:
            product = catalog_service.get_product_by_id(cart_item.product_id)
            if product and product.stock >= cart_item.quantity:
                order_items.append(OrderItem(
                    cart_item.product_id,
                    cart_item.size,
                    cart_item.quantity,
                    product.price
                ))

        if not order_items:
            return None

        order = Order(self._next_id, user_id, order_items, address, payment_method)
        self._next_id += 1
        self._orders.append(order)

        for item in order_items:
            product = catalog_service.get_product_by_id(item.product_id)
            if product:
                product.reduce_stock(item.quantity)

        return order

    def get_orders_by_user(self, user_id):
        return [order for order in self._orders if order.user_id == user_id]

    def get_all_orders(self):
        return self._orders.copy()

    def get_order_by_id(self, order_id):
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def update_order_status(self, order_id, status):
        order = self.get_order_by_id(order_id)
        if order:
            order.status = status
            return True
        return False



order_service = OrderService()