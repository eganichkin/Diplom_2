import allure
from data import BASE_URL, USER_URL, REGISTER_URL, LOGIN_URL
import json
import requests
from helper import UserDataGenerate


class UserMethods(UserDataGenerate):
    @allure.step('Инизиализация учётных данных нового пользователя, сгенерированных случайным образом в виде словаря.')
    def __init__(self):
        self.user_data = self.get_random_user_data()
        self.user_access_token = ''

    @allure.step('Получение пользовательской информации по email и паролю в виде словаря.')
    def get_email_password(self):
        return {"email": self.user_data['email'], "password": self.user_data['password']}

    @allure.step('Получение пользовательской информации по email и имени в виде словаря.')
    @allure.step('')
    def get_email_name(self):
        return {"email": self.user_data['email'], "name": self.user_data['name']}

    @allure.step('Получение информации по пользовательскому токену.')
    def get_user_access_token(self):
        return self.user_access_token

    @allure.step('Выполнение POST-запроса для создания пользователя, попытка получения его токена.')
    def post_create_user(self):
        headers = {"Content-type": "application/json"}
        response = requests.post(f'{BASE_URL}{REGISTER_URL}', data=json.dumps(self.user_data), headers=headers)
        if response.status_code == 200:
            self.user_access_token = response.json()['accessToken']
        return response

    @allure.step('Выполнение POST-запроса для логирования пользователя.')
    def post_login_user(self):
        data = self.get_email_password()
        headers = {"Content-type": "application/json"}
        response = requests.post(f'{BASE_URL}{LOGIN_URL}', data=json.dumps(data), headers=headers)
        return response

    @allure.step('Выполнение DELETE-запроса для удаления пользователя.')
    def delete_user(self):
        headers = {'Authorization': self.user_access_token}
        response = requests.delete(f'{BASE_URL}{USER_URL}', headers=headers)
        return response

    @allure.step('Выполнение PATCH-запроса для изменения данных пользователя.')
    def patch_update_user(self):
        data = self.get_email_name()
        headers = {"Content-type": "application/json"}
        if self.user_access_token:
            headers = {"Content-type": "application/json", "Authorization": self.user_access_token}

        response = requests.patch(f'{BASE_URL}{USER_URL}', data=json.dumps(data), headers=headers)
        return response

    @allure.step('Проверка корректности данных пользователя, полученных в случае успешного ответа.')
    def check_user_success_response(self, response):
        actual_value = response.json().get('user')
        expected_value = self.get_email_name()

        if actual_value == expected_value:
            return True
        return False
