import cv2
import json

from src import KEYS
from src.camera import Camera
from src.client import send_image
from src.logger import client_logger


if __name__ == '__main__':
    CONFIG_FNAME = 'client_config.json'

    with open(CONFIG_FNAME, 'r') as config_file:
        config = json.load(config_file)

    camera_id = config['camera_id']
    resolution = (config['frame_width'], config['frame_height'])
    camera = Camera(camera_id, resolution)

    while True:
        img = camera.get_frame()
        if img is None:
            client_logger.error(f'Cannot acces to camer by id: [{camera_id}]')
            break

        cv2.imshow('secure camera', img)
        pressed_key = cv2.waitKey(10)

        if pressed_key & 0xFF == KEYS.SPACE.value:
            client_logger.info('Sending image to server...')
            url = f'http://{config["server_host"]}:{config["server_port"]}/getimage'

            response = send_image(url, img)

            if 'error' in response:
                client_logger.error(response['error'])
            else:
                client_logger.info('Server received the image')

        elif pressed_key & 0xFF == KEYS.ESC.value:
            client_logger.info('Camera was stopped')
            break

    camera.close()
