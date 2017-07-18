from flask import Flask, current_app, request, json
import io
import model
import base64

app = Flask(__name__)


@app.route('/', methods=['POST'])
def style_transform():
    data = {}
    try:
        data = request.get_json()['data']
    except KeyError:
        return jsonify(status_code='400', msg='Bad Request'), 400

    data = base64.b64decode(data)  #Decode a Base64 encoded string.

    image = io.BytesIO(data)
    new_img = model.style_transform(image)
    
    return json.dumps({'data': base64.b64encode(new_img)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
