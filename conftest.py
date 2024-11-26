import pytest
from methods.user_methods import UserMethods
from methods.order_methods import OrderMethods


@pytest.fixture()
def user_methods():
    return UserMethods()


@pytest.fixture()
def order_methods():
    return OrderMethods()


@pytest.fixture()
def user(user_methods):
    user_methods.post_create_user()
    yield
    user_methods.delete_user()
