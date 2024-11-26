import allure
import pytest
from data import ResponseMessages
from models import user_models
from helper import JsonValidation


class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя.')
    @allure.description('Случайным образом генерируются данные для нового пользователя, '
                        'производится попытка создания уникального пользователя, '
                        'выполняется проверка на код 200 успешного выполнения, валидация тела ответа.')
    def test_create_user(self, user_methods):
        response = user_methods.post_create_user()
        assert response.status_code == 200
        assert user_methods.check_user_success_response(response)
        assert JsonValidation.assert_schema(response, user_models.UserAuthSchema)

    @allure.title('Проверка повторного создания уже зарешистрированного пользователя.')
    @allure.description('Выполняется запрос для создания нового пользователя, '
                        'после производится повторная попытка создания этого же пользователя, '
                        'выполняется проверка на код ошибки 403, валидация тела ответа и текста ошибки.')
    def test_create_two_users(self, user_methods):
        user_methods.post_create_user()
        response = user_methods.post_create_user()
        assert response.status_code == 403
        assert JsonValidation.assert_schema(response, user_models.UserErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_ALREADY_EXISTS)

    @allure.title('Проверка создания пользователя с незаненными значениями одного из обязательных полей.')
    @allure.description('Используя параметризацию выполняется попытка запроса пользователя с незаненными значениями '
                        'одного из обязательных полей: "email", "password", "name". '
                        'выполняется проверка на код ошибки 403, валидация тела ответа и текста ошибки.')
    @pytest.mark.parametrize(
        'empty_field_name',
        ["email", "password", "name"]
    )
    def test_create_courier_with_empty_fields(self, user_methods, empty_field_name):
        user_methods.user_data[empty_field_name] = ''
        response = user_methods.post_create_user()
        assert response.status_code == 403
        assert JsonValidation.assert_schema(response, user_models.UserErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_NOT_REQUIRED_FIELDS)
