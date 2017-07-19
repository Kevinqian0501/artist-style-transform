import numpy as np
import tensorflow as tf
import transform
import io
from PIL import Image, ImageOps

## need 3 dims img
def get_img(src, img_size=False):
   img = src  # Already pill image
   if not (len(img.shape) == 3 and img.shape[2] == 3):
       img = np.dstack((img,img,img))
 
   return img

## get 3d, np and rgb img
def get_rgb_np(img_in):
    img = Image.open(img_in).convert('RGB')
    img_np = np.array(img)
    return get_img(img_np)

## Trans image
def rundeeplearning(img_in, checkpoint_dir, batch_size=1):
   
    img = get_rgb_np(img_in) 
    img_shape = get_img(img).shape


    g = tf.Graph()
    soft_config = tf.ConfigProto(allow_soft_placement=True)
    config_mu =tf.ConfigProto(intra_op_parallelism_threads=16)
    config_ = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1, \
                        allow_soft_placement=True, device_count = {'CPU': 1})   
    soft_config.gpu_options.allow_growth = True
    with g.as_default(), \
            tf.Session(config=config_mu) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.placeholder(tf.float32, shape=batch_shape,
                                         name='img_placeholder')
        preds = transform.net(img_placeholder)
        saver = tf.train.Saver()
        # Load 
        saver.restore(sess, checkpoint_dir)
        X = np.zeros(batch_shape, dtype=np.float32)
        X[0] = img

        _preds = sess.run(preds, feed_dict={img_placeholder:X})
        img_np = np.clip(_preds[0], 0, 255).astype(np.uint8)
        img_out = Image.fromarray(img_np)
        buffer = io.BytesIO()
        img_out.save(buffer, format="PNG")
	
        return buffer
