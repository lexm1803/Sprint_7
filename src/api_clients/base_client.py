import requests


class BaseClient:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type':'application/json'})

    def build_url(self, path):
        return f'{self.BASE_URL}{path}'
    
    def get(self, path, params=None):
        url = self.build_url(path)
        return self.session.get(url, params=params)
    
    def post(self, path, json=None):
        url = self.build_url(path)
        return self.session.post(url, json=json)
    
    def put(self, path, json=None, params=None):
        url = self.build_url(path)
        return self.session.put(url, json=json, params=params)
    
    def delete(self, path, params=None):
        url = self.build_url(path)
        return self.session.delete(url, params=params)
    