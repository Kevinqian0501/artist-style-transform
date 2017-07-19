import os
import config
import logging
from flask import current_app, Flask, render_template, request
from io import BytesIO
from google.appengine.api import images
from google.appengine.ext import blobstore
import base64
import urllib2
from model import storage
import json
from model import firebase_api as fb
import pytz
import time
import datetime


app = Flask(__name__)
app.config.from_object(config)
logging.basicConfig(level=logging.DEBUG)

## upload img to bucket, return url and bucket_filepath
def upload_image_file(stream, filename, content_type):
    if not stream:
        return None


    bucket_filepath = storage.upload_file(
        stream,
        filename,
        content_type
    )

    logging.info(
        "Uploaded file %s as %s.", filename, bucket_filepath)

    blobstore_filename = '/gs{}'.format(bucket_filepath)
    blob_key = blobstore.create_gs_key(blobstore_filename)
    img_url = images.get_serving_url(blob_key, secure_url=True)
    return img_url, bucket_filepath

## send img and style to trans-service
def fetch_img(img_stream, style):
    # img_stream = Image.open(BytesIO(img_stream)).convert('RGB')
    server_url = current_app.config['PREDICTION_SERVICE_URL']
    req = urllib2.Request(server_url, json.dumps({'data': base64.b64encode(img_stream)}),
                          {'Content-Type': 'application/json'})
    data = {}
    try:
        f = urllib2.urlopen(req)
	json_data = json.loads(f.read());
	data = json_data['data']
	data = base64.b64decode(data)
    except urllib2.HTTPError as e:
        logging.exception(e)

    logging.info('img: %s', data )

    return data

def dump_result(bucket_filepath, image_url, new_image_url, style):
    timestamp = int(time.time())
    filename = bucket_filepath.split('/')[-1].split('.')[0]

    result = {
        filename: {
            'style' : style,
            'new_image_url': new_image_url,
            'image_url': image_url,
            'create_timestamp': timestamp
            }
        }
    return json.dumps(result)

def get_firebase_url(database):
    url = '%s/%s.json' % (config.FIREBASE_URL, database)
    logging.info('jirebase url is logging.info %s', url)
    return url

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        img = request.files.get('image')
        style = "cloud"

        img_stream = img.read()
        data = fetch_img(img_stream, style)	        

        filename = img.filename
        content_type = img.content_type
        img_url, bucket_filepath = upload_image_file(img_stream, filename, content_type)

	new_img = BytesIO(data)
        new_img_stream = new_img.read()
        new_filename = filename.split('.')[0] + '-' + style + '.' + filename.split('.')[1]
        new_content_type = content_type
        new_img_url, new_bucket_filepath = upload_image_file(new_img_stream, new_filename, new_content_type)

    	result = dump_result(bucket_filepath, img_url, new_img_url, style)

    	content = fb.firebase_patch(get_firebase_url('results'), result)

        #return render_template('view.html', image_url=img_url, predictions=predictions['predictions'])
        return render_template(
            'view.html', 
            image_url=img_url, new_image_url = new_img_url,
            style = style
        )    
    return render_template('form.html')


@app.errorhandler(500)
def server_error(e):
    logging.error('An error occurred during a request.')
    return 'An internal error occurred.', 500

