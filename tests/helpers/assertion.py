from requests import Response


def assert_status_code(response, expected_code):
    actual_code = response.status_code 
    if actual_code != expected_code:
        error_message = ''
        try:
            json_body = response.json()
            if 'message' in json_body:
                error_message = f': {json_body['message']}'
        except Exception:
            pass
        raise AssertionError(f'Ожидаемый статус-код: {expected_code}.'
                             f'Актуальный статус-код: {actual_code}, {error_message}'
                             f'url: {response.url}, метод: {response.request.method}')
    
def assert_response_has_key(response, key):
    try:
        json_body = response.json()
    except ValueError:
        raise AssertionError(f'JSON ответа не валиден: {response.text[:200]}')
    if key not in json_body:
        raise AssertionError(f'Ключ {key} не найден в ответе: {json_body}')
    
def assert_error_message(response, expected_message, expected_status=400):
    assert_status_code(response, expected_status)
    assert_response_has_key(response, 'message')
    actual_message = response.json()['message']
    if expected_message not in actual_message:
        raise AssertionError(f'Ожидаемое сообщение об ошибке: {expected_message}.'
                             f'Полученное сообщение об ошибке: {actual_message}.')
    