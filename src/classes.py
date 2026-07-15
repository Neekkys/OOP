from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный класс для класса Product"""

    def __init__(self, *args, **kwargs):
        super().__init__()

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class MixinLogConsole:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(MixinLogConsole, BaseProduct):
    """Класс для продукта"""

    name: str
    description: str
    __price: float
    quantity: int
    count_obj = 0
    product_dict: dict
    all_products: list

    def __init__(self, name, description, price, quantity=0):
        self.name = name
        self.description = description
        self.__price = price
        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        """Отображение цены продукта"""
        return self.__price

    @price.setter
    def price(self, value):
        """Сеттер новой цены для продукта. Невозможно установить цену ниже 0.
        Если новая цена меньше предыдущей, запрашивает подтверждение."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if hasattr(self, "_Product__price") and value < self.price:
            output = input("Цена товара ниже предыдущей. Для подтверждения напишите 'y'").strip().lower()
            if output != "y":
                print("Изменение цены отменено")
                return
        self.__price = value

    @classmethod
    def new_product(cls, product_dict, all_products=None):
        """Добавляет новый продукт в словарь с продуктами. Если продукт уже есть в словаре,
        обновляет количество продукта"""
        if all_products:
            for product in all_products:
                if product_dict["name"] == product.name:
                    product.quantity += product_dict["quantity"]
                    product.description = product_dict["description"]
                    if product_dict["price"] > product.price:
                        product.price = product_dict["price"]
                    return product

        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"],
        )

    def __str__(self):
        """Строковое отображение продукта в виде {цена}, {стоимость}, {остаток}"""
        return f"{self.name}, {self.price}. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Полная стоимость 2-х товаров с учетом количества на складе, если объекты сложения
        находятся в одной категории"""
        if not isinstance(other, type(self)):
            raise TypeError
        return self.__price * self.quantity + other.__price * other.quantity


class Category:
    """Категория техники и ее описание"""

    name: str
    description: str
    __products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    def add_product(self, product_obj):
        """Добавляет продукт в категорию. Принимает только объекты Product или его наследников"""
        if not isinstance(product_obj, Product):
            raise TypeError
        self.__products.append(product_obj)
        Category.product_count += 1

    @property
    def products(self):
        return [f"{p.name}, {p.price}. Остаток: {p.quantity} шт." for p in self.__products]

    def __str__(self):
        """Строковое отображение в виде {Категория}, {общее количество продуктов в классе}"""
        product_quantity = 0
        for p in self.__products:
            product_quantity += p.quantity
        return f"{self.name}, количество продуктов: {product_quantity}"


class Smartphone(Product):
    """Характеристики телефона"""

    efficiency: str
    model: str
    memory: str
    color: str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Трава газонная и ее характеристики"""

    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
