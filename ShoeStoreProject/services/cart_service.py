class CartItem:


    def __init__(self, product_id, size, quantity):
        self._product_id = product_id
        self._size = size
        self._quantity = quantity

    @property
    def product_id(self):
        return self._product_id

    @property
    def size(self):
        return self._size

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value > 0:
            self._quantity = value
        else:
            raise ValueError("Количеството трябва да е положително число")


class CartService:

    def __init__(self):
        self._carts = {}

    def get_cart(self, user_id):
        if user_id not in self._carts:
            self._carts[user_id] = []
        return self._carts[user_id]

    def add_to_cart(self, user_id, product_id, size, quantity=1):
        cart = self.get_cart(user_id)

        for item in cart:
            if item.product_id == product_id and item.size == size:
                item.quantity += quantity
                return True

        cart.append(CartItem(product_id, size, quantity))
        return True

    def remove_from_cart(self, user_id, product_id, size):
        cart = self.get_cart(user_id)
        for item in cart:
            if item.product_id == product_id and item.size == size:
                cart.remove(item)
                return True
        return False

    def update_quantity(self, user_id, product_id, size, quantity):
        cart = self.get_cart(user_id)
        for item in cart:
            if item.product_id == product_id and item.size == size:
                if quantity <= 0:
                    cart.remove(item)
                else:
                    item.quantity = quantity
                return True
        return False

    def clear_cart(self, user_id):
        if user_id in self._carts:
            self._carts[user_id] = []
            return True
        return False

    def get_cart_total(self, user_id, catalog_service):
        cart = self.get_cart(user_id)
        total = 0
        for item in cart:
            product = catalog_service.get_product_by_id(item.product_id)
            if product:
                total += product.price * item.quantity
        return total


cart_service = CartService()