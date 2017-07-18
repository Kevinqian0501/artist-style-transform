import numpy as np
import tensorflow as tf
#import transform
from PIL import Image, ImageOps

## need 3 dims img
def get_img(src, img_size=False):
   img = src  # Already pill image
   if not (len(img.shape) == 3 and img.shape[2] == 3):
       img = np.dstack((img,img,img))
 
   return img

## Evaluate image
def rundeeplearning(data_in, checkpoint_dir, device_t='/cpu:0', batch_size=1):
    img = get_img(data_in)
    img = Image.open(BytesIO(request.files['imagefile'].read())).convert('RGB')
    img_shape = img.shape
    g = tf.Graph()
    soft_config = tf.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True
    with g.as_default(), g.device(device_t), \
            tf.Session(config=soft_config) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.placeholder(tf.float32, shape=batch_shape,
                                         name='img_placeholder')
        preds = transform.net(img_placeholder)
        saver = tf.train.Saver()
        # Load 
        saver.restore(sess, checkpoint_dir)
        X = np.zeros(batch_shape, dtype=np.float32)
        img = get_img(data_in)
        assert img.shape == img_shape
        X[0] = img
        _preds = sess.run(preds, feed_dict={img_placeholder:X})
        out_img = np.clip(_preds[0], 0, 255).astype(np.uint8)
        return Image.fromarray(out_img)
