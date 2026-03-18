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
        return [f"{p.name}, {p.price}. Остаток: {p.quantity} шт.\n" for p in self.__products]


product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
product5 = Product('55" QLED 4K', "Фоновая подсветка и смарт", 150000.0, 8)

# print(product1.name)
# print(product1.description)
# print(product1.price)
# print(product1.quantity)
#
# print(product2.name)
# print(product2.description)
# print(product2.price)
# print(product2.quantity)
#
# print(product3.name)
# print(product3.description)
# print(product3.price)
# print(product3.quantity)

category1 = Category(
    "Смартфоны",
    "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    [product1, product2, product3],
)

# print(category1.name == "Смартфоны")
# print(category1.name)
# print(category1.description)
# print(len(category1._products))
# # print(category1.category_count)
# print(category1.product_count)


category2 = Category(
    "Телевизоры",
    "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
    [product4],
)

# print(category2.name)
# print(category2.description)
# print(len(category2._products))
# print(category2.get_products)
#
# print(Category.category_count)
# print(Category.product_count)
print("-------------------")
