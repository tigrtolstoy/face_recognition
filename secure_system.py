import io
import json
import numpy as np
from flask import Flask, request

from src.secure_server.server import IdentificationHandler


CONFIG_FNAME = 'server_config.json'

with open(CONFIG_FNAME, 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
identification_handler = IdentificationHandler(config['accuracy_thrashold'], 
                                               config['db_path'],
                                               config['path_to_save_photos'])


def decode_image(encoded_image):
    image = np.load(io.BytesIO(encoded_image))
    return image


@app.route('/')
def index():
    return {'response': 'index route'}


@app.route('/identificate', methods=['POST'])
def get_image():
    image = decode_image(request.data)
    employee_id = request.args['employee_id']
    ident_result = identification_handler.identificate(image, employee_id)
    return ident_result


if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'])
