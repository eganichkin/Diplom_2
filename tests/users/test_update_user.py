import allure
import pytest
from data import ResponseMessages
from models import user_models
from helper import JsonValidation


class TestUpdateUser:

    @allure.title('Проверка изменения данных пользователя с авторизацией.')
    @allure.description('Создаётся новый пользователь, производится логирование. Используя токен, при помощи '
                        'параметризации выполняется запрос для обновления одного из полей пользователя:"email", "name".'
                        'Производится проверка на код ответа 200, валидация тела ответа, проверка, что данные '
                        'дейсвительно изменились. Ранее созданный пользователь удаляется.')
    @pytest.mark.parametrize(
        'update_field_name',
        ["email", "name"]
    )
    def test_update_user_with_authorization(self, user_methods, user, update_field_name):
        user_methods.user_data[update_field_name] = "update_" + user_methods.user_data[update_field_name]
        response = user_methods.patch_update_user()
        assert response.status_code == 200
        assert JsonValidation.assert_schema(response, user_models.GetUserInfoSchema)
        assert user_methods.check_user_success_response(response)

    @allure.title('Проверка изменения данных пользователя без авторизации.')
    @allure.description('Предварительно создаётся новый пользователь. Без токена авторизации при помощи параметризации'
                        'выполняется запрос для обновления одного из полей пользователя:"email", "name".'
                        'Производится проверка на код ответа 401, валидация тела ответа и текста ошибки. '
                        'Ранее созданный пользователь удаляется.')
    @pytest.mark.parametrize(
        'update_field_name',
        ["email", "name"]
    )
    def test_update_user_without_authorization(self, user_methods, update_field_name):
        user_methods.user_data[update_field_name] = "update_" + user_methods.user_data[update_field_name]
        response = user_methods.patch_update_user()
        assert response.status_code == 401
        assert JsonValidation.assert_schema(response, user_models.UserErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_SHOULD_BE_AUTHORIZED)
