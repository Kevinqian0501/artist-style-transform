from flask import Flask, current_app, request, jsonify
import io
import json
#import model
import base64
from PIL import Image
import numpy as np
import logging

app = Flask(__name__)


@app.route('/', methods=['POST'])
def style_transform():
    data = {}
    try:
        data = request.get_json()['data']
       # style = request.get_json()['style']
    except KeyError:
        return jsonify(status_code='400', msg='Bad Request'), 400

    #### current_app.logger.info('Style: %s', style)
    
    data = base64.b64decode(data)  #Decode a Base64 encoded string.
    #img_in = io.BytesIO(data)
    
    img_out = model.rundeeplearning(data)

    data_out = base64.b64encode(img_out)  #Decode a Base64 encoded string.    
    return json.dumps({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
