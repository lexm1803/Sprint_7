from requests import Response
from .base_client import BaseClient


class CourierClient(BaseClient):
    
    def register(self, *, login, password, firstName):
        payload = {
            'login': login,
            'password': password,
            'firstName': firstName
        }
        return self.post('/courier', json=payload)
    
    def login(self, login, password):
        payload = {
            'login': login,
            'password': password
        }
        return self.post('/courier/login', json=payload)
    
    def delete(self, courier_id):
        return super().delete(f'/courier/{courier_id}')
    