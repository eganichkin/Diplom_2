BASE_URL = 'https://stellarburgers.nomoreparties.site/api'
AUTH_URL = '/auth'
USER_URL = '/auth/user'
LOGIN_URL = '/auth/login'
REGISTER_URL = '/auth/register'
ORDERS_URL = '/orders'
INVALID_HASH_INGREDIENT = '61c0c5a71d1f82001bdaaa73123'

ORDER_INFO = {
    "ingredients": [
        "61c0c5a71d1f82001bdaaa73",
        "61c0c5a71d1f82001bdaaa75",
        "61c0c5a71d1f82001bdaaa6c"
    ]
}


class ResponseMessages:
    USER_ALREADY_EXISTS = 'User already exists'
    USER_NOT_REQUIRED_FIELDS = 'Email, password and name are required fields'
    USER_INCORRECT_EMAIL_PASS = 'email or password are incorrect'
    USER_SHOULD_BE_AUTHORIZED = 'You should be authorised'
    USER_EMAIL_ALREADY_EXISTS = 'User with such email already exists'
    ORDER_NOT_INGREDIENTS = 'Ingredient ids must be provided'
    ORDER_INTERNAL_SERVER_ERROR = 'Internal Server Error'
