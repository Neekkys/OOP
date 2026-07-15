import pytest

from src.classes import Category, LawnGrass, Product, Smartphone


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
        f"{product_samsung.name}, {product_samsung.price}. Остаток: {product_samsung.quantity} шт.",
        f"{product_iphone.name}, {product_iphone.price}. Остаток: {product_iphone.quantity} шт.",
        f"{product_xiaomi.name}, {product_xiaomi.price}. Остаток: {product_xiaomi.quantity} шт.",
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
def test_product_initt(product_samsung):
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
    expected_line = f"{product_tv.name}, {product_tv.price}. Остаток: {product_tv.quantity} шт."
    assert category_smartphones.products[-1] == expected_line


def test_products_format(category_smartphones, product_samsung, product_iphone, product_xiaomi):
    expected = [
        f"{product_samsung.name}, {product_samsung.price}. Остаток: {product_samsung.quantity} шт.",
        f"{product_iphone.name}, {product_iphone.price}. Остаток: {product_iphone.quantity} шт.",
        f"{product_xiaomi.name}, {product_xiaomi.price}. Остаток: {product_xiaomi.quantity} шт.",
    ]
    assert category_smartphones.products == expected


def test_str_representation(product_apple):
    """Проверка строкового представления продукта"""
    expected = "Яблоко, 100.0. Остаток: 5 шт."
    assert str(product_apple) == expected


def test_add_two_products(product_apple, product_banana):
    """Проверка сложения полной стоимости двух продуктов"""
    # Стоимость яблок: 100 * 5 = 500
    # Стоимость бананов: 80 * 10 = 800
    # Сумма: 1300
    assert product_apple + product_banana == 1300.0


def test_add_with_updated_price(product_apple, product_banana):
    """Сложение должно корректно работать после изменения цены"""
    product_apple.price = 120.0  # новая цена выше предыдущей
    # Стоимость яблок: 120 * 5 = 600
    # Стоимость бананов: 80 * 10 = 800
    # Сумма: 1400
    assert product_apple + product_banana == 1400.0


def test_str_representation_2(category_fruits):
    """Проверка строкового представления категории с суммой количества всех продуктов"""
    # Яблоко 5 шт + Банан 10 шт = 15
    expected = "Фрукты, количество продуктов: 15"
    assert str(category_fruits) == expected


def test_str_after_adding_product(category_fruits):
    """Проверка обновления строки после добавления нового продукта"""
    orange = Product("Апельсин", "Сладкие апельсины", 90.0, 7)
    category_fruits.add_product(orange)
    # Теперь количество: 5 + 10 + 7 = 22
    expected = "Фрукты, количество продуктов: 22"
    assert str(category_fruits) == expected


def test_str_empty_category():
    """Проверка категории без продуктов"""
    empty_cat = Category("Пустая", "Нет товаров", [])
    assert str(empty_cat) == "Пустая, количество продуктов: 0"


def test_add_same_subclass():
    """Сложение двух смартфонов (одинаковый подкласс) работает"""
    s1 = Smartphone("A", "desc", 1000, 2, 90.0, "model", 64, "red")
    s2 = Smartphone("B", "desc", 2000, 3, 95.0, "model2", 128, "blue")
    result = s1 + s2
    # 1000*2 + 2000*3 = 2000 + 6000 = 8000
    assert result == 8000.0


def test_add_different_subclass_raises_typeerror():
    """Сложение смартфона и газонной травы вызывает TypeError, т.к. типы разные"""
    s1 = Smartphone("A", "desc", 1000, 1, 90.0, "model", 64, "red")
    g1 = LawnGrass("Grass", "desc", 100, 5, "RU", "7d", "green")
    with pytest.raises(TypeError):
        s1 + g1


def test_add_with_unrelated_type_raises_typeerror():
    """Сложение продукта с не-продуктом вызывает TypeError"""
    p = Product("P", "d", 100, 1)
    with pytest.raises(TypeError):
        p + "строка"
    with pytest.raises(TypeError):
        p + 42


def test_add_product_accepts_subclass():
    """В категорию можно добавить наследника Product (Smartphone, LawnGrass)"""
    cat = Category("Test", "desc", [])
    phone = Smartphone("Phone", "desc", 100, 1, 95.0, "X", 64, "black")
    grass = LawnGrass("Grass", "desc", 50, 2, "RU", "7d", "green")

    cat.add_product(phone)
    cat.add_product(grass)
    assert len(cat.products) == 2


def test_add_product_rejects_non_product():
    """При попытке добавить не продукт (число, строка, список) вызывается TypeError"""
    cat = Category("Test", "desc", [])
    with pytest.raises(TypeError):
        cat.add_product("не продукт")
    with pytest.raises(TypeError):
        cat.add_product(123)
    with pytest.raises(TypeError):
        cat.add_product(["список"])


def test_add_product_rejects_object_other_class():
    """Даже объект другого класса, не связанного с Product, вызывает TypeError"""

    class SomeForeign:
        pass

    obj = SomeForeign()
    cat = Category("Test", "desc", [])
    with pytest.raises(TypeError):
        cat.add_product(obj)


def test_smartphone_init():
    s = Smartphone("Samsung", "256GB", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")
    # наследованные атрибуты
    assert s.name == "Samsung"
    assert s.description == "256GB"
    assert s.price == 180000.0
    assert s.quantity == 5
    # собственные атрибуты
    assert s.efficiency == 95.5
    assert s.model == "S23 Ultra"
    assert s.memory == 256
    assert s.color == "Серый"


def test_smartphone_is_product():
    s = Smartphone("A", "desc", 100, 1, 90.0, "M", 64, "red")
    assert isinstance(s, Product)
    assert isinstance(s, Smartphone)


def test_smartphone_price_setter_works():
    s = Smartphone("A", "desc", 1000, 1, 90.0, "M", 64, "red")
    s.price = 1200  # повышение
    assert s.price == 1200
    s.price = -10  # отрицательная — не изменится
    assert s.price == 1200


def test_lawn_grass_init():
    g = LawnGrass("Трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert g.name == "Трава"
    assert g.description == "Элитная"
    assert g.price == 500.0
    assert g.quantity == 20
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "Зеленый"


def test_lawn_grass_is_product():
    g = LawnGrass("T", "d", 10, 1, "RU", "3d", "green")
    assert isinstance(g, Product)
    assert isinstance(g, LawnGrass)


def test_lawn_grass_str_uses_product_str():
    g = LawnGrass("Трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert str(g) == "Трава, 500.0. Остаток: 20 шт."


def test_product_creation_logs_repr(capsys):
    """При создании Product в консоль печатается repr объекта"""
    p = Product("Телефон", "Описание", 15000, 3)
    captured = capsys.readouterr()
    expected_repr = "Product(Телефон, Описание, 15000, 3)\n"
    assert captured.out == expected_repr
    # Дополнительно проверяем, что атрибуты установлены корректно
    assert p.name == "Телефон"
    assert p.price == 15000
    assert p.quantity == 3


def test_smartphone_creation_logs_repr(capsys):
    """При создании Smartphone в консоль печатается repr объекта (с параметрами родителя)"""
    s = Smartphone("iPhone", "Флагман", 80000, 2, 95.5, "15 Pro", 256, "Silver")
    captured = capsys.readouterr()
    # repr из миксина использует только атрибуты name, description, price, quantity
    expected_repr = "Smartphone(iPhone, Флагман, 80000, 2)\n"
    assert captured.out == expected_repr
    # Проверяем, что специфичные атрибуты смартфона тоже установлены
    assert s.efficiency == 95.5
    assert s.model == "15 Pro"
    assert s.memory == 256
    assert s.color == "Silver"


def test_lawn_grass_creation_logs_repr(capsys):
    """При создании LawnGrass в консоль печатается repr объекта"""
    g = LawnGrass("Газонная трава", "Элитная", 500, 20, "Россия", "7 дней", "Зеленый")
    captured = capsys.readouterr()
    expected_repr = "LawnGrass(Газонная трава, Элитная, 500, 20)\n"
    assert captured.out == expected_repr
    # Дополнительная проверка атрибутов
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "Зеленый"


def test_multiple_creations_log_each(capsys):
    """При создании нескольких объектов каждый выводит свой repr"""
    Product("A", "desc1", 100, 1)
    Product("B", "desc2", 200, 2)
    captured = capsys.readouterr()
    expected = "Product(A, desc1, 100, 1)\nProduct(B, desc2, 200, 2)\n"
    assert captured.out == expected
