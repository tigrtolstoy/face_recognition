import io
import requests
import numpy as np


def encode_image(image):
    bytes_stream = io.BytesIO()
    np.save(bytes_stream, image)
    encoded_image = bytes_stream.getvalue()
    return encoded_image

    

def send_image(url, image):
    encoded_image = encode_image(image)
    try:
        response = requests.post(url, data=encoded_image)
        return response
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection error'}