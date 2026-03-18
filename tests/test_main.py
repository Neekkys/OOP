import pytest
from main import Product, Category


def test_product_init(product_samsung):
    assert product_samsung.name == "Samsung Galaxy S23 Ultra"
    assert product_samsung.description == "256GB, Серый цвет, 200MP камера"
    assert product_samsung.price == 180000.0
    assert product_samsung.quantity == 5


def test_category_initialization(category_smartphones, product_samsung, product_iphone, product_xiaomi):
    """Проверяем атрибуты категории и список продуктов"""
    assert category_smartphones.name == "Смартфоны"
    assert category_smartphones.description.startswith("Смартфоны")

    products_list = category_smartphones.products
    assert len(products_list) == 3

    expected_strings = [
        f"{product_samsung.name}, {product_samsung.price}. Остаток: {product_samsung.quantity} шт.\n",
        f"{product_iphone.name}, {product_iphone.price}. Остаток: {product_iphone.quantity} шт.\n",
        f"{product_xiaomi.name}, {product_xiaomi.price}. Остаток: {product_xiaomi.quantity} шт.\n",
    ]
    assert products_list == expected_strings


def test_category_count_increases():
    """Проверяем, что при создании категорий счётчик category_count увеличивается"""
    # Создаём первую категорию
    cat1 = Category("Cat1", "Desc1", [])
    assert cat1.name == "Cat1"
    assert Category.category_count == 1
    # Создаём вторую категорию
    cat2 = Category("Cat2", "Desc2", [])
    assert cat2.name == "Cat2"
    assert Category.category_count == 2


def test_product_count_increases():
    """Проверяем, что при создании категорий с продуктами счётчик product_count увеличивается на число продуктов"""
    # Создаём продукты
    p1 = Product("P1", "D1", 100, 1)
    p2 = Product("P2", "D2", 200, 2)

    # Категория с двумя продуктами
    cat1 = Category("Cat1", "Desc1", [p1, p2])
    assert cat1.name == "Cat1"
    assert Category.product_count == 2

    # Категория без продуктов
    cat2 = Category("Cat2", "Desc2", [])
    assert cat2.name == "Cat2"
    assert Category.product_count == 2  # не должно измениться

    # Категория с одним продуктом
    p3 = Product("P3", "D3", 300, 3)
    cat3 = Category("Cat3", "Desc3", [p3])
    assert cat3.name == "Cat3"
    assert Category.product_count == 3


def test_product_count_with_existing_fixtures(category_smartphones, category_tvs):
    """
    Используем фикстуры для проверки подсчёта продуктов.
    Фикстура reset_counts обнулила счётчики перед тестом.
    """
    # category_smartphones создана с 3 продуктами
    # category_tvs создана с 1 продуктом
    # Всего продуктов = 4
    assert Category.product_count == 4


def test_category_count_with_fixtures(category_smartphones, category_tvs):
    """Проверяем счётчик категорий с фикстурами"""
    # Две категории созданы фикстурами
    assert Category.category_count == 2


def test_category_without_products():
    """Проверяем категорию без продуктов"""
    cat = Category("Empty", "No products", [])
    assert cat.name == "Empty"
    assert len(cat.products) == 0
    # Счётчик категорий должен увеличиться (сброшен до 0 перед тестом)
    assert Category.category_count == 1
    # Счётчик продуктов не увеличился
    assert Category.product_count == 0


# ---------- Product ----------
def test_product_init(product_samsung):
    assert product_samsung.name == "Samsung Galaxy S23 Ultra"
    assert product_samsung.description == "256GB, Серый цвет, 200MP камера"
    assert product_samsung.price == 180000.0
    assert product_samsung.quantity == 5


@pytest.mark.parametrize(
    "new_price,expected,confirm,should_change",
    [
        (200000.0, 200000.0, None, True),  # повышение
        (150000.0, 150000.0, "y", True),  # понижение с подтверждением
        (150000.0, 180000.0, "n", False),  # понижение без подтверждения
        (0, 180000.0, None, False),  # неположительная
        (-10, 180000.0, None, False),
    ],
)
def test_product_price_setter(product_samsung, monkeypatch, capsys, new_price, expected, confirm, should_change):
    old_price = product_samsung.price
    if confirm is not None:
        monkeypatch.setattr("builtins.input", lambda _: confirm)
    product_samsung.price = new_price
    captured = capsys.readouterr()
    if new_price <= 0:
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
    elif not should_change:
        assert "Изменение цены отменено" in captured.out
    assert product_samsung.price == expected


def test_new_product_behavior(product_tv):
    # Создание нового продукта
    data_new = {"name": "New", "description": "Desc", "price": 500, "quantity": 2}
    new_prod = Product.new_product(data_new)
    assert isinstance(new_prod, Product) and new_prod.name == "New"

    # Обновление существующего с более высокой ценой
    existing = [product_tv]
    data_higher = {"name": '55" QLED 4K', "description": "Higher", "price": 150000.0, "quantity": 3}
    res = Product.new_product(data_higher, existing)
    assert res is product_tv
    assert product_tv.quantity == 7 + 3
    assert product_tv.description == "Higher"
    assert product_tv.price == 150000.0

    # Обновление с более низкой ценой (цена не меняется)
    data_lower = {"name": '55" QLED 4K', "description": "Lower", "price": 100000.0, "quantity": 1}
    res = Product.new_product(data_lower, existing)
    assert res is product_tv
    assert product_tv.quantity == 10 + 1  # 7+3=10, +1=11
    assert product_tv.price == 150000.0  # не изменилась


# ---------- Category ----------
def test_category_init(category_smartphones):
    assert category_smartphones.name == "Смартфоны"
    assert len(category_smartphones.products) == 3


def test_category_counters(category_smartphones, category_tvs):
    # Сброс счётчиков выполняется автоматически (autouse)
    assert Category.category_count == 2
    assert Category.product_count == 4  # 3 (смартфоны) + 1 (телевизоры)


def test_add_product(category_smartphones, product_tv):
    old_len = len(category_smartphones.products)
    category_smartphones.add_product(product_tv)
    assert len(category_smartphones.products) == old_len + 1
    expected_line = f"{product_tv.name}, {product_tv.price}. Остаток: {product_tv.quantity} шт.\n"
    assert category_smartphones.products[-1] == expected_line


def test_products_format(category_smartphones, product_samsung, product_iphone, product_xiaomi):
    expected = [
        f"{product_samsung.name}, {product_samsung.price}. Остаток: {product_samsung.quantity} шт.\n",
        f"{product_iphone.name}, {product_iphone.price}. Остаток: {product_iphone.quantity} шт.\n",
        f"{product_xiaomi.name}, {product_xiaomi.price}. Остаток: {product_xiaomi.quantity} шт.\n",
    ]
    assert category_smartphones.products == expected
