from flask import Flask, current_app, request, json
import io
import model
import base64
from PIL import Image
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['POST'])
def style_transform():
    data = {}
    try:
        data = request.get_json()['data']
        style = request.get_json()['style']
    except KeyError:
        return jsonify(status_code='400', msg='Bad Request'), 400

    data = base64.b64decode(data)  #Decode a Base64 encoded string.

    image = Image.open(io.BytesIO(data).convert('RGB')
    in_img = np.array(img)
    new_img = model.style_transform(in_img, style)
    
    return json.dumps({'data': base64.b64encode(new_img)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
