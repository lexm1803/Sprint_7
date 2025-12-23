import pytest
import allure
from src.api_clients.courier_client import CourierClient
from tests.helpers.assertion import assert_status_code, assert_response_has_key, assert_error_message


@allure.epic('API тесты')
@allure.feature('Курьеры')
@allure.story('Авторизация курьера')
class TestCourierLogin:

    @allure.title('Успешная авторизация курьера')
    @allure.description('Проверка возврата статус-кода 200 и id курьера при авторизации')
    def test_login_success(self, courier_client: CourierClient, registred_courier):
        
        with allure.step(f'Отправка POST на /courier/login с логином {registred_courier['login']}'):
            response = courier_client.login(
                login=registred_courier['login'],
                password=registred_courier['password']
            )
        
        with allure.step('Проверка статус-кода 200 при успешной авторизации'):
            assert_status_code(response, 200)

        with allure.step('Проверка наличия id курьера, его корректность'):
            assert_response_has_key(response, 'id')
            courier_id = response.json()['id']
            assert isinstance(courier_id, int), f'Id должен быть целым числом (int), получен {type(courier_id)}'
            assert courier_id == registred_courier['id'], \
                f'Id из логина ({courier_id}) не соответствует id существующего курьера ({registred_courier['id']})'
            
    @pytest.mark.parametrize('missing_field', [
        ('login', {'password': '123'}),
        ('password', {'login': 'Test'})
    ], ids=['non login', 'non password'])
    @allure.title('Авторизация без обязательного поля {missing_field[0]}')
    @allure.description('Ошибка при попытке авторизации без обязательного поля')
    def test_login_missing_field_fails(self, courier_client: CourierClient, missing_field):
        field_name, parital_data = missing_field

        with allure.step(f'Отправка запроса авторизации без поля {field_name}'):
            login_value = parital_data.get('login')
            password_value = parital_data.get('password')
            response = courier_client.login(
                login=login_value,
                password=password_value
            )

        with allure.step('Ожидание статус-кода 400 с сообщением об ошибке'):
            assert_status_code(response, 400)
            assert_error_message(response, 'Недостаточно данных для входа', expected_status=400)

    @allure.title('Авторизация с неверным паролем учетной записи')
    @allure.description('Ошибка при попытке авторизации с существующим логином и несуществующим паролем')
    def test_login_error_password_fails(self, courier_client: CourierClient, registred_courier):
        wrong_password = registred_courier['password'] + '_wrong'
        
        with allure.step('Отправка POST на /courier/login с некорректным паролем'):
            response = courier_client.login(
                login=registred_courier['login'],
                password=wrong_password
            )

        with allure.step('Ожидание статус-кода 404 с сообщением об ошибке'):
            assert_status_code(response, 404)
            assert_error_message(response, 'Учетная запись не найдена', expected_status=404)
        
    @allure.title('Авторизация с неверным логином')
    @allure.description('Ошибка при попытке авторизации с несуществующим логином')
    def test_error_login_fails(self, courier_client: CourierClient):
        fake_login = 'non_existant_login' + 'x' * 5
        fake_password = 'any_password'
        
        with allure.step('Отправка POST на /courier/login с несуществующим логином'):
            response = courier_client.login(
                login=fake_login,
                password=fake_password
            )

        with allure.step('Ожидание статус-кода 404 с сообщением об ошибке'):
            assert_status_code(response, 404)
            assert_error_message(response, 'Учетная запись не найдена', expected_status=404)
        