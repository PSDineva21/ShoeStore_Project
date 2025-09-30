class Product:


    def __init__(self, id, name, description, color, sizes, price, stock, category, gender, image_url=None):
        self._id = id
        self._name = name
        self._description = description
        self._color = color
        self._sizes = sizes
        self._price = price
        self._stock = stock
        self._category = category
        self._gender = gender
        self._image_url = image_url or self._get_default_image()

    def _get_default_image(self):

        image_map = {
            'sports': '/static/images/sports-shoe.jpg',
            'formal': '/static/images/formal-shoe.jpg',
            'boots': '/static/images/boots.jpg',
            'sandals': '/static/images/sandals.jpg'
        }
        return image_map.get(self._category, '/static/images/default-shoe.jpg')


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

    @property
    def category(self):
        return self._category

    @property
    def gender(self):
        return self._gender

    @property
    def image_url(self):
        return self._image_url


    @name.setter
    def name(self, value):
        if value and len(value) >= 2:
            self._name = value
        else:
            raise ValueError("Името трябва да е поне 2 символа")

    @description.setter
    def description(self, value):
        self._description = value

    @color.setter
    def color(self, value):
        if value and len(value) >= 2:
            self._color = value
        else:
            raise ValueError("Цвятът трябва да е поне 2 символа")

    @sizes.setter
    def sizes(self, value):
        if value and isinstance(value, list) and len(value) > 0:
            self._sizes = value
        else:
            raise ValueError("Трябва да има поне един размер")

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

    @category.setter
    def category(self, value):
        valid_categories = ['sports', 'formal', 'boots', 'sandals']
        if value in valid_categories:
            self._category = value
        else:
            raise ValueError("Невалидна категория")

    @gender.setter
    def gender(self, value):
        valid_genders = ['men', 'women', 'unisex']
        if value in valid_genders:
            self._gender = value
        else:
            raise ValueError("Невалиден пол")

    @image_url.setter
    def image_url(self, value):
        self._image_url = value

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
            # СПОРТНИ ОБУВКИ
            ("Nike Air Max", "Спортни обувки за бягане", "бели", [40, 41, 42, 43, 44], 120.00, 15, 'sports', 'men',
             "/static/images/products/nike_air_max.jpg"),
            ("Adidas Runfalcon", "Леки спортни обувки", "черни", [36, 37, 38, 39, 40], 95.00, 12, 'sports', 'women',
             "/static/images/products/adidas_runfalcon.jpg"),
            ("Puma RS-X", "Ретро спортни обувки", "сини", [39, 40, 41, 42, 43], 110.00, 8, 'sports', 'unisex',
             "/static/images/products/puma_rsx.jpg"),
            ("Nike Revolution", "Удобни обувки за фитнес", "розови", [36, 37, 38, 39], 85.00, 10, 'sports', 'women',
             "/static/images/products/nike_revolution.jpg"),

            # ОФИЦИАЛНИ ОБУВКИ
            ("Dolce and Gabbana", "Класически официални обувки", "черни", [40, 41, 42, 43, 44], 150.00, 8, 'formal', 'men',
             "/static/images/products/dolce_and_gabbana.jpg"),
            ("YSL", "Елегантни официални обувки", "черни", [36, 37, 38, 39], 180.00, 6, 'formal', 'women',
             "/static/images/products/ysl_heels.jpg"),
            ("Ducavelli", "Официални обувки", "кафяви", [41, 42, 43, 44], 135.00, 7, 'formal', 'men',
             "/static/images/products/ducavelli.jpg"),
            ("Red", "Луксозни официални обувки", "червени", [37, 38, 39, 40], 220.00, 4, 'formal', 'women',
             "/static/images/products/red_heels.jpg"),

            # БОТУШИ
            ("Timberland Premium", "Зимни ботуши с кожена подметка", "кафяви", [40, 41, 42, 43, 44], 200.00, 5, 'boots',
             'men',
             "/static/images/products/timberland.jpg"),
            ("UGG Classic", "Топли зимни ботуши", "бели", [36, 37, 38, 39], 180.00, 8, 'boots', 'women',
             "/static/images/products/ugg_classic.jpg"),
            ("Grand attack", "Класически ботуши", "кафяви", [39, 40, 41, 42, 43], 160.00, 6, 'boots', 'unisex',
             "/static/images/products/grand.jpg"),
            ("Lowa", "Планински ботуши", "тъмно сиви", [41, 42, 43, 44], 145.00, 4, 'boots', 'men',
             "/static/images/products/lowa.jpg"),

            # ЛЕТНИ ОБУВКИ
            (
            "Crocs", "Класически сандали", "кафяви", [39, 40, 41, 42, 43], 90.00, 12, 'sandals', 'unisex',
            "/static/images/products/crocs_men.jpg"),
            ("Havaianas Slim", "Джапанки за плаж", "черни", [36, 37, 38, 39, 40], 25.00, 20, 'sandals', 'women',
             "/static/images/products/havainas_slim.jpg"),
            ("Nike", "Чехли", "черни", [40, 41, 42, 43, 44], 65.00, 10, 'sandals', 'men',
             "/static/images/products/nike_sandals.jpg"),
            ("Crocs Classic", "Удобни летни обувки", "бели", [37, 38, 39, 40], 40.00, 15, 'sandals', 'women',
             "/static/images/products/crocs_woman.jpg")
        ]

        for product_data in sample_products:
            if len(product_data) == 9:
                name, desc, color, sizes, price, stock, category, gender, image_url = product_data
                self.add_product(name, desc, color, sizes, price, stock, category, gender, image_url)
            else:
                name, desc, color, sizes, price, stock, category, gender = product_data
                self.add_product(name, desc, color, sizes, price, stock, category, gender)
    @property
    def products(self):
        return self._products.copy()

    def add_product(self, name, description, color, sizes, price, stock, category, gender, image_url=None):
        product = Product(self._next_id, name, description, color, sizes, price, stock, category, gender, image_url)
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

        if not search_term or not search_term.strip():
            return self._products

        results = []
        search_lower = search_term.strip().lower()

        for product in self._products:
            product_name = product.name.lower() if product.name else ""
            product_color = product.color.lower() if product.color else ""
            product_description = product.description.lower() if product.description else ""
            product_category = self.get_category_name(product.category).lower() if product.category else ""


            if (search_lower in product_name or
                    search_lower in product_color or
                    search_lower in product_description or
                    search_lower in product_category):
                results.append(product)

        return results

    def get_products_by_category(self, category):
        return [p for p in self._products if p.category == category]

    def get_products_by_gender(self, gender):
        return [p for p in self._products if p.gender == gender or p.gender == 'unisex']

    def get_products_by_category_and_gender(self, category, gender):
        return [p for p in self._products if p.category == category and (p.gender == gender or p.gender == 'unisex')]

    def get_categories(self):
        return ['sports', 'formal', 'boots', 'sandals']

    def get_category_name(self, category):
        category_names = {
            'sports': 'Спортни обувки',
            'formal': 'Официални обувки',
            'boots': 'Ботуши',
            'sandals': 'Летни обувки'
        }
        return category_names.get(category, category)

    def get_gender_name(self, gender):
        gender_names = {
            'men': 'Мъжки',
            'women': 'Дамски',
            'unisex': 'Унисекс'
        }
        return gender_names.get(gender, gender)

    def sort_products(self, products, key='name', reverse=False):

        def quick_sort(arr):
            if len(arr) <= 1:
                return arr

            pivot = arr[len(arr) // 2]
            try:
                pivot_value = getattr(pivot, key)
            except AttributeError:

                return arr

            left = [p for p in arr if getattr(p, key) < pivot_value]
            middle = [p for p in arr if getattr(p, key) == pivot_value]
            right = [p for p in arr if getattr(p, key) > pivot_value]

            if reverse:
                return quick_sort(right) + middle + quick_sort(left)
            else:
                return quick_sort(left) + middle + quick_sort(right)

        return quick_sort(products.copy())


catalog_service = CatalogService()