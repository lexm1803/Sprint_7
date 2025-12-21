import pytest
import allure
from src.api_clients.order_client import OrderClient
from tests.helpers.assertion import assert_status_code, assert_response_has_key, assert_error_message
from tests.helpers.generators import generate_order_data


@allure.epic('API тесты')
@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestOrderCreation:

    @pytest.mark.parametrize('colors, description', [
        (["BLACK"], "Один цвет: BLACK"),
        (["GREY"], "Один цвет: GREY"),
        (["BLACK", "GREY"], "Оба цвета: BLACK и GREY"),
        ([], "Без указания цвета")
    ])
    @allure.title('Создание заказа с цветами {description}')
    @allure.description('Проверка создания заказа с разными вариантами поля "color"')
    def test_order_creation_with_colors(self, order_client: OrderClient, colors, description):
        order_data = generate_order_data()
        order_data['color'] = colors

        with allure.step(f'Отправка POST с цветами {colors}'):
            response = order_client.create(order_data)

        with allure.step('Проверка статус-кода 201'):
            assert_status_code(response, 201)

        with allure.step('Проверка наличия трек-номера заказа'):
            assert_response_has_key(response, 'track')
            track = response.json()['track']
            assert isinstance(track, int), f'Номер заказа должен быть числом, получен {type(track)}'
            assert track > 0, f'Номер заказа должен быть положительным, получен {track}'
