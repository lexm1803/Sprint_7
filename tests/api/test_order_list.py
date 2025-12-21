import pytest
import allure
from src.api_clients.order_client import OrderClient
from tests.helpers.assertion import assert_status_code, assert_response_has_key, assert_error_message


@allure.epic('API тесты')
@allure.feature('Заказы')
@allure.story('Получение списка заказов')
class TestOrdersList:

    @allure.title('Получение списка всех заказов')
    @allure.description('Проверка получения списка заказов')
    def test_get_order_list_succes(self, order_client: OrderClient):

        with allure.step('Отправка GET на получение списка заказов'):
            response = order_client.get_list()

        with allure.step('Проверка статус-кода 200'):
            assert_status_code(response, 200)

        with allure.step('Проверка структуры ответа'):
            json_body = response.json()
            with allure.step('Проверка поля "orders"'):
                assert 'orders' in json_body, 'В ответе нет поля "orders"'
                assert isinstance(json_body['orders'], list), '"orders" не является списком'
            
            with allure.step('Проверка поля "pageInfo"'):
                assert 'pageInfo' in json_body, 'В ответе нет поля "pageInfo"'
                pageInfo = json_body['pageInfo']
                assert 'page' in pageInfo and isinstance(pageInfo['page'], int), 'В ответе нет поля "page" или в нем содержится не число'
                assert 'total' in pageInfo and isinstance(pageInfo['total'], int), 'В ответе нет поля "total" или в нем содержится не число'
                assert 'limit' in pageInfo and isinstance(pageInfo['limit'], int), 'В ответе нет поля "limit" или в нем содержится не число'

            with allure.step('Проверка поля "availableStations"'):
                assert 'availableStations' in json_body, 'В ответе нет поля "availableStations"'
                stations = json_body['availableStations']
                assert isinstance(stations, list), '"availableStations" не является списком'
                if stations:
                    first_station = stations[0]
                    assert 'name' in first_station, 'В ответе нет поля "name"'
                    assert 'number' in first_station, 'В ответе нет поля "number"'
                    assert 'color' in first_station, 'В ответе нет поля "color"'

    @allure.title('Получение списка заказов курьера')
    @allure.description('Проверка получения списка заказов курьера')
    def test_get_order_by_courier_id(self, order_client: OrderClient, registred_courier):
        courier_id = registred_courier['id']
        with allure.step(f'Отправка GET с courier_id = {courier_id}'):
            response = order_client.get_list(courier_id=courier_id)
        
        with allure.step('Проверка статус-кода 200'):
            assert_status_code(response, 200)
        
        with allure.step(f'Проверка отсутствия заказов у курьера {courier_id}'):
            orders = response.json()['orders']
            assert isinstance(orders, list), '"orders" не является списком'
            assert len(orders) == 0, f'У курьера {courier_id} не должно быть заказов, вернулся(лось) {len(orders)} заказ(ов).'
            