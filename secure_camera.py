import cv2
import json
from time import monotonic

from src import KEYS
from src.secure_client.camera import Camera
from src.secure_client.client import send_image, dump_identification_info
from src.logger import client_logger


if __name__ == '__main__':
    CONFIG_FNAME = 'client_config.json'

    SERVER_URL = 'http://{}:{}/identificate?employee_id={}'

    with open(CONFIG_FNAME, 'r') as config_file:
        config = json.load(config_file)

    wrong_ident_timeout = config['wrong_ident_timeout']
    camera_id = config['camera_id']
    resolution = (config['frame_width'], config['frame_height'])

    camera = Camera(camera_id, resolution)

    identification_available = True
    last_wrong_identification_time = 0

    while True:
        img = camera.get_frame()
        if img is None:
            client_logger.error(
                f'Не удается получить доступ к камере по id: [{camera_id}]')
            break

        cv2.imshow('secure camera', img)
        pressed_key = cv2.waitKey(10)

        if pressed_key & 0xFF == KEYS.SPACE.value:
            # при нажатии пробела фотография отправляется на сервер,
            # если в течение wrong_ident_timeout секунд не было
            # проваленой идентификации

            if not identification_available:
                current_time = monotonic()
                elapsed_time = current_time - last_wrong_identification_time
                if elapsed_time > wrong_ident_timeout:
                    identification_available = True
                else:
                    block_time = round(wrong_ident_timeout - elapsed_time, 2)
                    print(
                        f'Идентфификация недоступна в течение {block_time} секунд')
                    client_logger.info(
                        'Попытка идентификации во время блокировки')
                    continue

            person_id = input('Введите персональный идентификатор: ')

            if not len(person_id):
                print('Персональный идентификатор не может быть пустым.')

                print('В идентификации отказано.')
                identification_available = False
                last_wrong_identification_time = monotonic()
                client_logger.info('Попытка идентификации во время блокировки')

            client_logger.info('Отправка фотогорафии на сервер')
            
            url = SERVER_URL.format(
                config['server_host'],
                config['server_port'], 
                person_id
            )

            response = send_image(url, img)

            if 'error' in response:  # если сервер недоступен
                client_logger.error(response['error'])
            else:  # получаем ответ от сервера
                client_logger.info('Сервер произвел идентификацию')

                status = response['response']['status']
                msg = response['response']['msg']
                conf = response['response']['coincidence_confidence']
                client_logger.info(f'STATUS: {status} - MSG: {msg} - COINCIDENCE_CONFIDENCE: {conf}%')

                if status == 'unsuccessful':  # если идентификация провалилась, ставим блок на wrong_ident_timeout
                    identification_available = False
                    last_wrong_identification_time = monotonic()

                # сохраняем результат в json-файл
                dump_identification_info(response['response'])
            

        elif pressed_key & 0xFF == KEYS.ESC.value:
            client_logger.info('Работа камеры остановлена')
            break

    camera.close()
