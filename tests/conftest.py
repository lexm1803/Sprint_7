import pytest
import requests
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
    
    if reg_resp.status_code != 201: 
        raise requests.exceptions.HTTPError(f'Ошибка регистрации. Статус: {reg_resp.status_code}, тело ответа: {reg_resp.json()}')
    login_resp = courier_client.login(
        login= data['login'],
        password= data['password']
    )
    
    if login_resp.status_code != 200:
        raise requests.exceptions.HTTPError(f'Ошибка авторизации. Статус: {login_resp.status_code}, тело ответа: {login_resp.json()}')
    
    courier_id = login_resp.json()['id']
    data['id'] = courier_id
    yield data

    del_resp = courier_client.delete(courier_id)
    if del_resp.status_code != 200:
        print(f'ВНИМАНИЕ! Ошибка удаления курьера {courier_id}. \n'
              f'Статус: {del_resp.status_code}. Тело: {del_resp.json()}')
        
@pytest.fixture
def registr_courier(courier_client: CourierClient):
    data = {}
    def reg(login, password, firstName):
        data['login'] = login
        data['password'] = password
        data['firstName'] = firstName
        response = courier_client.register(login=login, password=password, firstName=firstName)
        return response
    
    yield reg
    resp_login = courier_client.login(login=data['login'], password=data['password'])
    if resp_login.status_code != 200:
        raise requests.exceptions.HTTPError(f'Id курьера не был получен для удаления. Статус-код ответа {resp_login.status_code}')
    courier_id = resp_login.json()['id']
    resp_delete = courier_client.delete(courier_id)
    if resp_delete.status_code != 200:
        print(f'Курьер {courier_id} не был удален')
    else:
        print(f'Курьер {courier_id} удален')

@pytest.fixture
def create_orders(order_client: OrderClient):
    data = {}
    def create(order_data):
        response = order_client.create(order_data=order_data)
        data['track'] = response.json()['track']
        return response
    
    yield create
    resp_cancelled = order_client.cancel_order(data['track'])
    if resp_cancelled.status_code != 200:
        print(f'Заказ {data["track"]} не был отменен')