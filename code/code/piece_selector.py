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

class Fuck:
    def __init__(self):
        print " "

        feature_chnl = 8

        feature_layer_1 = 32
        feature_layer_2 = 128

        feature_layer_soft = 256
        feature_layer_final = 90

        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()
        # tf.reset_default_graph()
        # print tf.get_default_session()
        # paras
        # 32? to be determined
        self.W_conv1 = weight_varible([3, 3, feature_chnl, feature_layer_1])
        self.b_conv1 = bias_variable([feature_layer_1])

        # conv layer-1
        self.x = tf.placeholder(tf.float32, [None, 9*10*feature_chnl])
        self.x_image = tf.reshape(self.x, [-1, 10, 9, feature_chnl])

        self.h_conv1 = tf.nn.relu(conv2d(self.x_image, self.W_conv1) + self.b_conv1)

        # conv layer-2
        self.W_conv2 = weight_varible([3, 3, feature_layer_1, feature_layer_2])
        self.b_conv2 = bias_variable([feature_layer_2])

        self.h_conv2 = tf.nn.relu(conv2d(self.h_conv1, self.W_conv2) + self.b_conv2)

        # full connection
        self.W_fc1 = weight_varible([10 * 9 * feature_layer_2, feature_layer_soft])
        self.b_fc1 = bias_variable([feature_layer_soft])

        self.h_conv2_flat = tf.reshape(self.h_conv2, [-1, 10 * 9 * feature_layer_2])
        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_conv2_flat, self.W_fc1) + self.b_fc1)

        # output layer: softmax
        self.W_fc2 = weight_varible([feature_layer_soft, feature_layer_final])
        self.b_fc2 = bias_variable([feature_layer_final])

        self.y_conv = tf.nn.softmax(tf.matmul(self.h_fc1, self.W_fc2) + self.b_fc2)


    def init_piece_selector(self):
        # self.sess.run(tf.global_variables_initializer())
        # print self.sess
        with self.sess.as_default():       
            saver = tf.train.Saver()
            saver.restore(self.sess, '../model/my-model-piece_selector-001')

    def init_piece_selector_with_version(self,version):
        # self.sess.run(tf.global_variables_initializer())
        # print self.sess
        self.sess.run(tf.initialize_all_variables())
        with self.sess.as_default():       
            saver = tf.train.Saver()
            saver.restore(self.sess, '../model/my-model-piece_selector-' + str(version))
        
    def close_piece_selector(self):
        with self.sess.as_default():
            tf.reset_default_graph()
            self.sess.close()

    def piece_selector_nn(self, fen):
        output = extract_features_piece(fen)
        feature = np.zeros((1, 720))
        feature[0] = output[0:-1].split(',')
        with self.sess.as_default():
            prediction = self.y_conv.eval(feed_dict={self.x: feature})
            prediction = np.reshape(prediction, (10, 9)).astype(np.float32)

        return prediction