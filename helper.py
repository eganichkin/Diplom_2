import random


class JsonValidation:
    @staticmethod
    def assert_schema(response, model):
        body = response.text
        return model.model_validate_json(body, strict=True)

    @staticmethod
    def check_error_response(response, expected_error_msg):
        if response.json().get('message') == expected_error_msg:
            return True
        return False


class UserDataGenerate:
    @staticmethod
    def get_random_number():
        return str(random.randint(10000, 99999))

    def get_random_user_data(self):
        return {"email": 'email_' + self.get_random_number() + '@yandex.ru',
                "password": 'password_' + self.get_random_number(),
                "name": 'name_' + self.get_random_number()}
