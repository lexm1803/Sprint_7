import pytest
from src.api_clients.courier_client import CourierClient
from src.api_clients.order_client import OrderClient
from tests.helpers.generators import generate_courier_data


@pytest.fixture
def courier_client():
    return CourierClient()

@pytest.fixture
def order_client():
    return OrderClient()

@pytest.fixture
def registred_courier(courier_client):
    data = generate_courier_data()
    reg_resp = courier_client.register(
        login= data['login'],
        password= data['password'],
        firstName=data['firstName']
    )
    
    assert reg_resp.status_code == 201, \
        f'Ошибка регистрации. Статус: {reg_resp.status_code}, тело ответа: {reg_resp.json()}'
    login_resp = courier_client.login(
        login= data['login'],
        password= data['password']
    )
    
    assert login_resp.status_code == 200, \
        f'Ошибка авторизации. Статус: {login_resp.status_code}, тело ответа: {login_resp.json()}'
    
    courier_id = login_resp.json()['id']
    data['id'] = courier_id
    yield data

    del_resp = courier_client.delete(courier_id)
    if del_resp.status_code != 200:
        print(f'ВНИМАНИЕ! Ошибка удаления курьера {courier_id}. \n'
              f'Статус: {del_resp.status_code}. Тело: {del_resp.json()}')
        