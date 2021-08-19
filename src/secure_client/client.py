import io
import json
import requests
import numpy as np
from datetime import datetime


def encode_image(image):
    bytes_stream = io.BytesIO()
    np.save(bytes_stream, image)
    encoded_image = bytes_stream.getvalue()
    return encoded_image


def send_image(url, image):
    encoded_image = encode_image(image)
    try:
        response = requests.post(url, data=encoded_image)
        if response.status_code == 500:
            return {'error': 'Ошибка на сервере'}
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'error': 'Ошибка подключения к серверу'}


def dump_identification_info(identification_info):
    current_time = datetime.now()
    current_time = current_time.strftime('%Y-%m-%d__%H:%M:%S')
    info_fname = f'{current_time}_identification_info.json'
    with open(info_fname, 'w') as ident_info_file:
        json.dump(identification_info, ident_info_file, ensure_ascii=False)
