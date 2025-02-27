"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


def new_product():
    return Product("postcard", 10, "Just a postcard", 5000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000) is True
        assert product.check_quantity(500) is True
        # assert product.check_quantity(1001) is False
        # assert product.check_quantity(0) is False
        # assert product.check_quantity(-1) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.buy(1000) is True
        assert product.buy(500) is True

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        assert product.buy(1001) is ValueError
        # assert product.buy(0) is ValueError
        # assert product.buy(-1) is ValueError


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 2
        cart.add_product(product)
        assert cart.products[product] == 3
        cart.add_product(new_product, buy_count=5)
        assert cart.products[new_product] == 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=5)
        assert cart.products[product] == 5
        cart.remove_product(product, remove_count=5)
        assert cart.products[product] == 0

    def test_clear(self, cart, product):
        cart.add_product(product, buy_count=2)
        cart.add_product(new_product(), buy_count=3)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product):
        cart.add_product(product, buy_count=2)
        cart.add_product(new_product(), buy_count=3)
        assert cart.get_total_price() == 100 * 2 + 10 * 3

    def test_buy(self, cart, product):
        cart.add_product(product, buy_count=2)
        # cart.add_product(new_product, buy_count=10)
        assert cart.buy() == "Покупка успешно завершена!"
        cart.add_product(product, buy_count=50000)
        assert cart.buy() is ValueError
