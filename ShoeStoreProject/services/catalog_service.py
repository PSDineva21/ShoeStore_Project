class Product:


    def __init__(self, id, name, description, color, sizes, price, stock):
        self._id = id
        self._name = name
        self._description = description
        self._color = color
        self._sizes = sizes
        self._price = price
        self._stock = stock

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def color(self):
        return self._color

    @property
    def sizes(self):
        return self._sizes

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    @name.setter
    def name(self, value):
        if value and len(value) >= 2:
            self._name = value
        else:
            raise ValueError("Името трябва да е поне 2 символа")

    @price.setter
    def price(self, value):
        if value >= 0:
            self._price = value
        else:
            raise ValueError("Цената не може да е отрицателна")

    @stock.setter
    def stock(self, value):
        if value >= 0:
            self._stock = value
        else:
            raise ValueError("Наличността не може да е отрицателна")

    def reduce_stock(self, quantity):
        if self._stock >= quantity:
            self._stock -= quantity
            return True
        return False


class CatalogService:


    def __init__(self):
        self._products = []
        self._next_id = 1
        self._initialize_sample_products()

    def _initialize_sample_products(self):
        sample_products = [
            ("Спортни обувки Nike", "Удобни обувки за спорт", "черни", [38, 39, 40, 41, 42], 89.99, 15),
            ("Официални обувки", "Елегантни обувки за офис", "кафяви", [39, 40, 41, 42, 43], 120.50, 8),
            ("Мартеници", "Летни обувки за почивка", "сини", [36, 37, 38, 39], 45.99, 20),
            ("Ботуши", "Зимни ботуши", "черни", [37, 38, 39, 40], 150.00, 5),
            ("Баскетболни обувки", "Обувки за баскетбол", "червени", [40, 41, 42, 43, 44], 110.00, 12)
        ]

        for name, desc, color, sizes, price, stock in sample_products:
            self.add_product(name, desc, color, sizes, price, stock)

    @property
    def products(self):
        return self._products.copy()

    def add_product(self, name, description, color, sizes, price, stock):
        product = Product(self._next_id, name, description, color, sizes, price, stock)
        self._next_id += 1
        self._products.append(product)
        return product

    def get_product_by_id(self, product_id):
        for product in self._products:
            if product.id == product_id:
                return product
        return None

    def update_product(self, product_id, **kwargs):
        product = self.get_product_by_id(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            return True
        return False

    def delete_product(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            self._products.remove(product)
            return True
        return False

    def search_products(self, search_term):
        if not search_term:
            return self._products

        results = []
        search_lower = search_term.lower()

        for product in self._products:
            if (search_lower in product.name.lower() or
                    search_lower in product.color.lower() or
                    search_lower in product.description.lower()):
                results.append(product)

        return results

    def sort_products(self, key='name', reverse=False):
        products = self._products.copy()

        def quick_sort(arr):
            if len(arr) <= 1:
                return arr

            pivot = arr[len(arr) // 2]
            pivot_value = getattr(pivot, key)

            left = [p for p in arr if getattr(p, key) < pivot_value]
            middle = [p for p in arr if getattr(p, key) == pivot_value]
            right = [p for p in arr if getattr(p, key) > pivot_value]

            if reverse:
                return quick_sort(right) + middle + quick_sort(left)
            else:
                return quick_sort(left) + middle + quick_sort(right)

        return quick_sort(products)


catalog_service = CatalogService()