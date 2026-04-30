class Product:
    """Класс для продукта"""

    name: str
    description: str
    __price: float
    quantity: int
    count_obj = 0
    product_dict: dict
    all_products: list

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
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
        """Добавляет продукт в список продуктов"""
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


if __name__ == '__main__':
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")

    smart_sum = smartphone1 + smartphone2
    print(smart_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")