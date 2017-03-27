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


feature_chnl = 8

feature_layer_1 = 32
feature_layer_2 = 128

feature_layer_soft = 256
feature_layer_final = 90

tf.reset_default_graph()
sess_p = tf.InteractiveSession()

# paras
# 32? to be determined
W_conv1_p = weight_varible([3, 3, feature_chnl, feature_layer_1])
b_conv1_p = bias_variable([feature_layer_1])

# conv layer-1
x_p = tf.placeholder(tf.float32, [None, 9*10*feature_chnl])
x_image_p = tf.reshape(x, [-1, 10, 9, feature_chnl])

h_conv1_p = tf.nn.relu(conv2d(x_image_p, W_conv1_p) + b_conv1_p)

# conv layer-2
W_conv2_p = weight_varible([3, 3, feature_layer_1, feature_layer_2])
b_conv2_p = bias_variable([feature_layer_2])

h_conv2_p = tf.nn.relu(conv2d(h_conv1_p, W_conv2_p) + b_conv2_p)

# full connection
W_fc1_p = weight_varible([10 * 9 * feature_layer_2, feature_layer_soft])
b_fc1_p = bias_variable([feature_layer_soft])

h_conv2_flat_p = tf.reshape(h_conv2_p, [-1, 10 * 9 * feature_layer_2])
h_fc1_p = tf.nn.relu(tf.matmul(h_conv2_flat_p, W_fc1_p) + b_fc1_p)

# output layer: softmax
W_fc2_p = weight_varible([feature_layer_soft, feature_layer_final])
b_fc2_p = bias_variable([feature_layer_final])

y_conv_p = tf.nn.softmax(tf.matmul(h_fc1_p, W_fc2_p) + b_fc2_p)

sess_p.run(tf.global_variables_initializer())

def init_piece_selector():
    # create model saver
    saver = tf.train.Saver()
    with sess_p.as_default():
        saver.restore(sess, '../model/my-model-piece_selector')
    
def close_piece_selector():
    sess_p.close()

def piece_selector_nn(fen):
    output = extract_features_piece(fen)
    feature = np.zeros((1, 720))
    feature[0] = output[0:-1].split(',')

    prediction = y_conv_p.eval(feed_dict={x_p: feature})
    prediction = np.reshape(prediction, (10, 9)).astype(np.float32)

    return prediction