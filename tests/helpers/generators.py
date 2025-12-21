import random
import string
from datetime import datetime, timedelta


def generate_random_string(lenght):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(lenght))

def generate_courier_data():
    return {
        'login': generate_random_string(10),
        'password': generate_random_string(10),
        'firstName': generate_random_string(8)
    }

def generate_order_data(courier_id=None):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    return {
        'firstName': generate_random_string(6).capitalize(), 
        'lastName': generate_random_string(8).capitalize(),
        'address': f'ул.{generate_random_string(5).capitalize()}, д.{random.randint(1, 100)}',
        'metroStation': str(random.randint(1, 200)),
        'phone': f'+7{random.randint(9000000000, 9999999999)}',
        'rentTime': random.randint(1, 7),
        'deliveryDate': tomorrow,
        'comment': f'test_order_by: {generate_random_string(5)}'
    }
