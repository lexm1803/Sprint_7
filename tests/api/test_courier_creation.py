import pytest
import allure
from src.api_clients.courier_client import CourierClient
from tests.helpers.generators import generate_courier_data, generate_random_string
from tests.helpers.assertion import assert_status_code, assert_response_has_key, assert_error_message


@allure.epic('API тесты')
@allure.feature('Курьеры')
@allure.story('Регистрация курьера')
class TestCourierCreation:

    @allure.title('Успешная регистрация курьера')
    @allure.description('Проверка успешного создания курьера при передаче данных для регистрации')
    def test_register_success(self, courier_client: CourierClient):
        data = generate_courier_data()

        with allure.step(f'Отправка POST на URL /courier с данными: {data}'):
            response = courier_client.register(
                login=data['login'],
                password=data['password'],
                firstName=data['firstName']
            )
        
        with allure.step('Проверка статуса 201'):
            assert_status_code(response, 201)

        with allure.step('Проверка тела ответа: ok - True'):   
            assert_response_has_key(response, 'ok')
            assert response.json()['ok'] is True
    
    @allure.title('Ошибка при регистрации существующего курьера')
    @allure.description('Проверка ошибки 409 при попытке регистрации курьера с существующими в базе данными')
    def test_register_duplicate_fails(self, courier_client: CourierClient):
        data = generate_courier_data()

        with allure.step(f'Регистрация курьера: логин - {data['login']}'):
            registration_1 = courier_client.register(
                login=data['login'],
                password=data['password'],
                firstName=data['firstName']
            )
            assert_status_code(registration_1, 201)

        with allure.step(f'Повторная регистрация курьера: логин - {data['login']}'):
            registration_2 = courier_client.register(
                login=data['login'],
                password=data['password'],
                firstName=data['firstName']
            )

        with allure.step('Провека ошибки регистрации курьера с уже существующим логином: статус-код 409'):
            assert_status_code(registration_2, 409)
            assert_error_message(registration_2, 'Этот логин уже используется', expected_status=409)

    @pytest.mark.parametrize('missing_field', [
        ('login', {'password': '123', 'firstName': 'Test'}), 
        ('password', {'login': generate_random_string(8), 'firstName': 'Test'}),
    ], ids=['non login', 'non password'])
    @allure.title('Проверка регистрации без обязательного поля {missing_field[0]}')
    @allure.description('Проверка статус-кода 400 при отсутствиии обязательного поля')
    def test_register_field_fails(self, courier_client: CourierClient, missing_field):
        field_name, parital_data=missing_field

        with allure.step(f'Отправка POST /courier без поля {field_name}'):
            login_value = parital_data.get('login')
            password_value = parital_data.get('password')
            firstName_value = parital_data.get('firstName')
            response = courier_client.register(
                login=login_value,
                password=password_value,
                firstName=firstName_value
            )
        
        with allure.step('Ожидание статус-кода 400 с сообщением об ошибке'):
            assert_status_code(response, 400)
            assert_error_message(response, 'Недостаточно данных для создания учетной записи', expected_status=400)
        