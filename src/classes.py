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
        self.price = price
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
        return f'{self.name}, {self.price}. Остаток: {self.quantity} шт.'


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
        self.__products.append(product_obj)
        Category.product_count += 1

    @property
    def products(self):
        return [f"{p.name}, {p.price}. Остаток: {p.quantity} шт." for p in self.__products]

    def __str__(self):
        product_quantity = 0
        for p in self.__products:
            product_quantity += p.quantity
        return f"{self.name}, количество продуктов: {product_quantity}"

