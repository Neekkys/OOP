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
    assert len(category_smartphones.products) == 3
    # Проверяем, что продукты в категории именно те, которые ожидаем
    assert category_smartphones.products[0] == product_samsung
    assert category_smartphones.products[1] == product_iphone
    assert category_smartphones.products[2] == product_xiaomi


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
