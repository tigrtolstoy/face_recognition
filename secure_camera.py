import cv2
import json

from src import KEYS
from src.camera import Camera
from src.client import send_image
from src.logger import client_logger


CONFIG_FNAME = 'client_config.json'

with open(CONFIG_FNAME, 'r') as config_file:
    config = json.load(config_file)

camera_id = config['camera_id']

camera = Camera(camera_id)


while True:
    img = camera.get_frame()
    if img is None:
        client_logger.error(f'Cannot acces to camer by id: [{camera_id}]')
        break

    cv2.imshow('secure camera', img)
    pressed_key = cv2.waitKey(10)

    if pressed_key & 0xFF == KEYS.SPACE.value:
        send_image('secure_system_url', img)
        client_logger.info('Image sended to server')
    elif pressed_key & 0xFF == KEYS.ESC.value:
        client_logger.info('Camera was stopped')
        break


camera.close()
