import allure
import pytest
from data import ResponseMessages
from models import user_models
from helper import JsonValidation


class TestLoginUser:

    @allure.title('Проверка логирования под сушествующим пользователем.')
    @allure.description('Предварительно создаётся новый пользователь, выполняется запрос для логирования пользователя.'
                        'Производится проверка на код ответа 200, валидация тела ответа. '
                        'Ранее созданный пользователь удаляется.')
    def test_login_user(self, user_methods, user):
        response = user_methods.post_login_user()
        assert response.status_code == 200
        assert user_methods.check_user_success_response(response)
        assert JsonValidation.assert_schema(response, user_models.UserAuthSchema)

    @allure.title('Проверка логирования с незаполненным значением email или пароля.')
    @allure.description('Предварительно создаётся новый пользователь, используя параметризацию производится попытка '
                        'логирования пользователя с незаполненным значением одного из полей: "email", "password". '
                        'Выполняется проверка на код ошибки 401, валидация тела ответа и текста ошибки.'
                        'Ранее созданный пользователь удаляется.')
    @pytest.mark.parametrize(
        'empty_field_name',
        ["email", "password"]
    )
    def test_login_user_with_empty_fields(self, user_methods, empty_field_name):
        user_methods.user_data[empty_field_name] = ''
        response = user_methods.post_login_user()
        assert response.status_code == 401
        assert JsonValidation.assert_schema(response, user_models.UserErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_INCORRECT_EMAIL_PASS)

    @allure.title('Проверка логирования с некорректным значением логина или пароля.')
    @allure.description('Предварительно создаётся новый пользователь, используя параметризацию производится попытка '
                        'логирования пользователя с некорретно заполненным значением одного из полей: '
                        '"email", "password". Проверка на код ошибки 401, валидация тела ответа и текста ошибки.'
                        'Ранее созданный пользователь удаляется.')
    @pytest.mark.parametrize(
        'incorrect_field_name',
        ["email", "password"]
    )
    def test_login_user_with_incorrect_fields(self, user_methods, incorrect_field_name):
        user_methods.user_data[incorrect_field_name] = 'IncorrectValue'
        response = user_methods.post_login_user()
        assert response.status_code == 401
        assert JsonValidation.assert_schema(response, user_models.UserErrorSchema)
        assert JsonValidation.check_error_response(response, ResponseMessages.USER_INCORRECT_EMAIL_PASS)
