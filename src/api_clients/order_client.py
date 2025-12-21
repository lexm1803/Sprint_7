from requests import Response
from .base_client import BaseClient


class OrderClient(BaseClient):

    def create(self, order_data):
        return self.post('/orders', json=order_data)
    
    def get_list(self, courier_id=None, limit=30, page=0):
        params = {
            'limit': limit,
            'page': page
        }
        if courier_id is not None:
            params['courierId'] = courier_id
        return self.get('/orders', params=params)
    
    def get_by_track(self, track):
        return self.get('/orders/track', params={'t': track})
    
    def accept(self, order_id, courier_id):
        return self.put(f'/orders/accept/{order_id}', params={'courierId': courier_id})
    