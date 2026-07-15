import pytest

from main import Category, Product


@pytest.fixture
def product_samsung():
    """Фикстура, возвращающая экземпляр Product (Samsung)"""
    return Product(
        name="Samsung Galaxy S23 Ultra", description="256GB, Серый цвет, 200MP камера", price=180000.0, quantity=5
    )


@pytest.fixture
def product_iphone():
    """Фикстура для iPhone"""
    return Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)


@pytest.fixture
def product_xiaomi():
    """Фикстура для Xiaomi"""
    return Product(name="Xiaomi Redmi Note 11", description="1024GB, Синий", price=31000.0, quantity=14)


@pytest.fixture
def product_tv():
    """Фикстура для телевизора"""
    return Product(name='55" QLED 4K', description="Фоновая подсветка", price=123000.0, quantity=7)


@pytest.fixture
def category_smartphones(product_samsung, product_iphone, product_xiaomi):
    """Фикстура, возвращающая категорию с тремя продуктами"""
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации...",
        products=[product_samsung, product_iphone, product_xiaomi],
    )


@pytest.fixture
def category_tvs(product_tv):
    """Фикстура, возвращающая категорию с одним продуктом"""
    return Category(name="Телевизоры", description="Современный телевизор...", products=[product_tv])


@pytest.fixture(autouse=True)
def reset_category_counts():
    """
    Сбрасывает счётчики категорий и продуктов перед каждым тестом.
    """
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_apple():
    """Продукт 'Яблоко' с ценой 100 и количеством 5"""
    return Product("Яблоко", "Свежие зелёные яблоки", 100.0, 5)


@pytest.fixture
def product_banana():
    """Продукт 'Банан' с ценой 80 и количеством 10"""
    return Product("Банан", "Спелые бананы", 80.0, 10)


@pytest.fixture
def category_fruits(product_apple, product_banana):
    """Категория 'Фрукты' с двумя продуктами"""
    return Category("Фрукты", "Сезонные фрукты", [product_apple, product_banana])


@pytest.fixture
def zero_quantity():
    """Создается продукт с нулевым количеством"""
    return Product("Банан", "Спелые бананы", 80.0, 0)

@pytest.fixture
def some_products():
    """Категория с 3 разными продуктами"""
    return Category("some_name", "some_descr", [
        Product("Банан", "Спелые бананы", 200.0, 10),
        Product("Яблоко", "Свежие зелёные яблоки", 30.0, 5),
        Product("Арбузы", "Сочные арбузы", 70.0, 6)
    ])

@pytest.fixture
def category_zero_product():
    return Category("some_name", "some_descr", [])
