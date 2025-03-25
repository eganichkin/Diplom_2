import allure
from data import BASE_URL, ORDERS_URL, ORDER_INFO
import json
import requests


class OrderMethods:

    @allure.step('Инизиализация предварительно подготовленных данных по заказу в виде словаря.')
    def __init__(self):
        self.order_data = ORDER_INFO
        self.user_access_token = ''

    @allure.step('Выполнение POST-запроса для создания закза.')
    def post_create_order(self):
        headers = {"Content-type": "application/json"}
        if self.user_access_token:
            headers["Authorization"] = self.user_access_token

        response = requests.post(f'{BASE_URL}{ORDERS_URL}', data=json.dumps(self.order_data), headers=headers)
        return response

    @allure.step('Последовательное выполнение POST-запросов для создания закзов в количестве N штук.')
    def create_n_orders(self, n):
        for i in range(n):
            self.post_create_order()

    @allure.step('Выполнение GET-запроса для получения заказов для конкретного пользователя.')
    def get_list_orders(self):
        headers = {"Content-type": "application/json"}
        if self.user_access_token:
            headers["Authorization"] = self.user_access_token

        response = requests.get(f'{BASE_URL}{ORDERS_URL}', headers=headers)
        return response

    @allure.step('Проверка корректности данных заказа, полученных в случае успешного ответа.')
    def check_order_success_response(self, response, user_data):
        r = response.json()
        actual_list_ingredients = []

        for ingredient in r['order'].get('ingredients'):
            actual_list_ingredients.append(ingredient['_id'])

        expected_list_ingredients = self.order_data.get('ingredients')
        actual_list_ingredients.sort()
        expected_list_ingredients.sort()

        owner = r['order'].get('owner')
        if (actual_list_ingredients == expected_list_ingredients and
                owner['email'] == user_data['email'] and owner['name'] == user_data['name']):
            return True

        return False

    @staticmethod
    def check_user_orders_count(response, expected_value):
        actual_value = len(response.json().get('orders'))
        if actual_value == expected_value:
            return True
        return False
