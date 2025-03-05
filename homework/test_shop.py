"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
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
        assert product.check_quantity(1001) is False
        assert product.check_quantity(1000) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1) is True
        assert product.check_quantity(0) is True
        assert product.check_quantity(-1) is True

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.buy(500) is True
        assert product.buy(499) is True

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        assert product.buy(10001) is ValueError


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_with_quantity(self, cart, product):
        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 2

    def test_add_product_without_quantity(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

    def test_add_few_different_products(self, cart, product, new_product):
        cart.add_product(product, buy_count=2)
        cart.add_product(new_product, buy_count=5)
        assert cart.products[product] == 2
        assert cart.products[new_product] == 5

    def test_remove_few_products(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=5)
        assert cart.products[product] == 5

    def test_remove_all_products_without_count(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_all_products_with_count(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=10)
        assert product not in cart.products

    def test_more_products_then_in_cart(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=15)
        assert product not in cart.products

    def test_clear(self, cart, product, new_product):
        cart.add_product(product, buy_count=2)
        cart.add_product(new_product, buy_count=3)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product, new_product):
        temp_count_1 = 2
        temp_count_2 = 3
        cart.add_product(product, buy_count=temp_count_1)
        cart.add_product(new_product, buy_count=temp_count_2)
        assert cart.get_total_price() == product.price * temp_count_1 + new_product.price * temp_count_2

    def test_successfull_buy(self, cart, product, new_product):
        cart.add_product(product, buy_count=200)
        cart.add_product(new_product, buy_count=1000)
        assert cart.buy() == "Покупка успешно завершена!"
        assert product.quantity == 800
        assert new_product.quantity == 4000

    def test_unsuccessfull_buy(self, cart, product, new_product):
        cart.add_product(product, buy_count=50000)
        assert cart.buy() is ValueError

    def test_unsuccessfull_buy_with_two_products(self, cart, product, new_product):
        cart.add_product(product, buy_count=200)
        cart.add_product(product, buy_count=50000)
        assert cart.buy() is ValueError
        assert product.quantity == 1000
        assert new_product.quantity == 5000
