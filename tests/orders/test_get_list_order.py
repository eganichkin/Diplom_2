import allure
from helper import JsonValidation
from models import order_models
from data import ResponseMessages
import pytest


class TestGetListOrder:

    @allure.title('Проверка получения заказов конеретного пользователя с авторизацией.')
    @allure.description('Создаётся новый пользователь, производится логирование. Используя токен авторизации, '
                        'производтся запрос для создания N заказов и выполняется запрос для '
                        'получения заказов для конеретного пользователя.'
                        'Производится проверка на код ответа 200, валидация тела, сравнивается количество создаваемых '
                        'заказов и количество, отображаемое в ответе. Ранее созданный пользователь удаляется.')
    @pytest.mark.parametrize(
        'count_orders', [1, 3]
    )
    def test_get_list_orders_for_authorized_user(self, order_methods, user_methods, user, count_orders):
        order_methods.user_access_token = user_methods.get_user_access_token()
        order_methods.create_n_orders(count_orders)
        response = order_methods.get_list_orders()
        assert response.status_code == 200
        assert JsonValidation.assert_schema(response, order_models.UserOrdersSchema)
        assert order_methods.check_user_orders_count(response, count_orders)

    @allure.title('Проверка получения заказов без авторизации.')
    @allure.description('Создаётся новый пользователь, производится логирование. Без использования авторизации, '
                        'производтся запрос получения заказов. Производится проверка на код ответа 500, '
                        'валидация текста ошибки. Ранее созданный пользователь удаляется.')
    def test_get_list_orders_for_unauthorized_user(self, order_methods, user_methods):
        order_methods.user_access_token = user_methods.user_access_token
        response = order_methods.get_list_orders()
        assert response.status_code == 401
        assert JsonValidation.assert_schema(response, order_models.OrderErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_SHOULD_BE_AUTHORIZED)
