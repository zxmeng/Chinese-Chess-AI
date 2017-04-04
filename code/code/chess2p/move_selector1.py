import tensorflow as tf
import numpy as np
from information import *


def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

class Fuck1_m:
    def __init__(self, piece_type):
        self.piece_type =  piece_type

        feature_layer_1 = 32
        feature_layer_2 = 128

        feature_layer_soft = 256
        feature_layer_final = 90

        tf.reset_default_graph()
        self.sess_m = tf.InteractiveSession()

        self.W_conv1_m = weight_varible([3, 3, 9, feature_layer_1])
        self.b_conv1_m = bias_variable([feature_layer_1])

        # conv layer-1
        self.x_m = tf.placeholder(tf.float32, [None, 810])
        self.x_image_m = tf.reshape(self.x_m, [-1, 10, 9, 9])

        self.h_conv1_m = tf.nn.relu(conv2d(self.x_image_m, self.W_conv1_m) + self.b_conv1_m)

        # conv layer-2
        self.W_conv2_m = weight_varible([3, 3, feature_layer_1, feature_layer_2])
        self.b_conv2_m = bias_variable([feature_layer_2])

        self.h_conv2_m = tf.nn.relu(conv2d(self.h_conv1_m, self.W_conv2_m) + self.b_conv2_m)

        # full connection
        self.W_fc1_m = weight_varible([10 * 9 * feature_layer_2, feature_layer_soft])
        self.b_fc1_m = bias_variable([feature_layer_soft])

        self.h_conv2_m_flat = tf.reshape(self.h_conv2_m, [-1, 10 * 9 * feature_layer_2])
        self.h_fc1_m = tf.nn.relu(tf.matmul(self.h_conv2_m_flat, self.W_fc1_m) + self.b_fc1_m)

        # output layer: softmax
        self.W_fc2_m = weight_varible([feature_layer_soft, feature_layer_final])
        self.b_fc2_m = bias_variable([feature_layer_final])

        self.y_conv_m = tf.nn.softmax(tf.matmul(self.h_fc1_m, self.W_fc2_m) + self.b_fc2_m)

    def init_move_selector(self):
        # sess_m.run(tf.global_variables_initializer())
        with self.sess_m.as_default(): 
            saver = tf.train.Saver() 
            saver.restore(self.sess_m, '../model/my-model-' + self.piece_type + "-017")
            print tf.get_default_session()

    def close_move_selector(self):
        self.sess_m.close()

    def move_selector_nn(self, output):
        feature = np.zeros((1, 810))
        feature[0] = output[0:-1].split(',')
        with self.sess_m.as_default():
            prediction = self.y_conv_m.eval(feed_dict={self.x_m: feature})
            prediction = np.reshape(prediction, (10, 9)).astype(np.float32)
    
        return prediction

