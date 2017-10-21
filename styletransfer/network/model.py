import os
import tensorflow as tf

from config import config
from styletransfer.network.layer import _conv_layer, _residual_block, _conv_tranpose_layer
from styletransfer.utils.singleton import Singleton


class StyleModel(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.init_network()

    def init_network(self):
        print("Initialize network")
        tf.reset_default_graph()
        self.sess = tf.Session()

        self.img_placeholder = tf.placeholder(tf.float32, shape=config.CONTENT_SHAPE,
                                     name='img_placeholder')
        self.preds = feedfoward_net(self.img_placeholder)
        self.saver = tf.train.Saver()
        self.current_style = ""

    def load_style(self, style):
        if self.current_style == style:
            print("Same style, isn't needed loading ckpts")
            return

        path = os.path.join(config.CKPT_BASE, style)
        if os.path.isdir(path):
            ckpt = tf.train.get_checkpoint_state(path)
            if ckpt and ckpt.model_checkpoint_path:
                self.saver.restore(self.sess, ckpt.model_checkpoint_path)
            else:
                raise Exception("No checkpoint found...")
        else:
            self.saver.restore(self.sess, path)

    def feedfoward(self, img):
        _preds = self.sess.run(self.preds, feed_dict={self.img_placeholder: [img]})
        return _preds


def feedfoward_net(img):
    conv1 = _conv_layer(img, 32, 9, 1)
    conv2 = _conv_layer(conv1, 64, 3, 2)
    conv3 = _conv_layer(conv2, 128, 3, 2)
    resid1 = _residual_block(conv3, 3)
    resid2 = _residual_block(resid1, 3)
    resid3 = _residual_block(resid2, 3)
    resid4 = _residual_block(resid3, 3)
    resid5 = _residual_block(resid4, 3)
    conv_t1 = _conv_tranpose_layer(resid5, 64, 3, 2)
    conv_t2 = _conv_tranpose_layer(conv_t1, 32, 3, 2)
    conv_t3 = _conv_layer(conv_t2, 3, 9, 1, relu=False)
    preds = tf.nn.tanh(conv_t3) * 150 + 255. / 2
    return preds