import allure
from helper import JsonValidation
from models import order_models
from data import INVALID_HASH_INGREDIENT
from data import ResponseMessages


class TestCreateOrder:
    @allure.title('Проверка создания заказа под авторизованным пользователем.')
    @allure.description('Создаётся новый пользователь, производится логирование. Используя токен, создаётся заказ '
                        'с предварительно подготовленным списком ингредиентов.'
                        'Производится проверка на код ответа 200, валидация тела и текста ответа.'
                        'Ранее созданный пользователь удаляется.')
    def test_create_order_with_authorization(self, order_methods, user_methods, user):
        order_methods.user_access_token = user_methods.user_access_token
        response = order_methods.post_create_order()
        assert response.status_code == 200
        assert order_methods.check_order_success_response(response, user_methods.user_data)
        assert JsonValidation.assert_schema(response, order_models.GetOrderInfoSchema)

    @allure.title('Проверка создания заказа без авторизации.')
    @allure.description('Создаётся новый пользователь, без использования токена авторизации создаётся заказ '
                        'с предварительно подготовленным списком ингредиентов.'
                        'Производится проверка на код ответа 200, валидация тела и текста ответа.'
                        'Ранее созданный пользователь удаляется.')
    def test_create_order_without_authorization(self, order_methods):
        response = order_methods.post_create_order()
        assert response.status_code == 200
        assert JsonValidation.assert_schema(response, order_models.GetOrderInfoWithoutAuthSchema)

    @allure.title('Проверка создания заказа без ингрединтов.')
    @allure.description('Создаётся новый пользователь, производится логирование. Используя токен, создаётся заказ '
                        'с пустым списком ингредиентов.'
                        'Производится проверка на код ответа 400, валидация тела и текста ошибки.'
                        'Ранее созданный пользователь удаляется.')
    def test_create_order_without_ingredients(self, order_methods, user_methods, user):
        order_methods.user_access_token = user_methods.user_access_token
        order_methods.order_data["ingredients"] = []
        response = order_methods.post_create_order()
        assert response.status_code == 400
        assert JsonValidation.assert_schema(response, order_models.OrderErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.ORDER_NOT_INGREDIENTS)

    @allure.title('Проверка создания заказа с неверным хэшем ингрединтов.')
    @allure.description('Создаётся новый пользователь, производится логирование. Используя токен, создаётся заказ '
                        'с некорретно заполненной инфомарцией по одному ингредиенту (неверный хэш).'
                        'Производится проверка на код ответа 500, валидация текста ошибки.'
                        'Ранее созданный пользователь удаляется.')
    def test_create_order_incorrect_hash_ingredient(self, order_methods, user_methods, user):
        order_methods.user_access_token = user_methods.user_access_token
        order_methods.order_data["ingredients"].append(INVALID_HASH_INGREDIENT)
        response = order_methods.post_create_order()
        assert response.status_code == 500
        assert ResponseMessages.ORDER_INTERNAL_SERVER_ERROR in response.text

