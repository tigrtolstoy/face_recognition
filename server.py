import io
import json
import numpy as np
from flask import Flask, request



app = Flask(__name__)


def decode_image(encoded_image):
    image = np.load(io.BytesIO(encoded_image))
    return image


@app.route('/')
def index():
    return {'response': 'index route'}

@app.route('/getimage', methods=['POST'])
def get_image():
    image = decode_image(request.data)
    return {'response': {'image_shape': str(image.shape)}}



if __name__ == '__main__':
    CONFIG_FNAME = 'server_config.json'

    with open(CONFIG_FNAME, 'r') as config_file:
        config = json.load(config_file)
    
    app.run(host=config['host'], port=config['port'])
