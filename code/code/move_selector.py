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


feature_layer_1 = 32
feature_layer_2 = 128

feature_layer_soft = 256
feature_layer_final = 90

tf.reset_default_graph()
sess_m = tf.InteractiveSession()

# paras
# 32? to be determined
W_conv1_m = weight_varible([3, 3, 9, feature_layer_1])
b_conv1_m = bias_variable([feature_layer_1])

# conv layer-1
x_m = tf.placeholder(tf.float32, [None, 810])
x_image_m = tf.reshape(x_m, [-1, 10, 9, 9])

h_conv1_m = tf.nn.relu(conv2d(x_image_m, W_conv1_m) + b_conv1_m)

# conv layer-2
W_conv2_m = weight_varible([3, 3, feature_layer_1, feature_layer_2])
b_conv2_m = bias_variable([feature_layer_2])

h_conv2_m = tf.nn.relu(conv2d(h_conv1_m, W_conv2_m) + b_conv2_m)

# full connection
W_fc1_m = weight_varible([10 * 9 * feature_layer_2, feature_layer_soft])
b_fc1_m = bias_variable([feature_layer_soft])

h_conv2_m_flat = tf.reshape(h_conv2_m, [-1, 10 * 9 * feature_layer_2])
h_fc1_m = tf.nn.relu(tf.matmul(h_conv2_m_flat, W_fc1_m) + b_fc1_m)

# output layer: softmax
W_fc2_m = weight_varible([feature_layer_soft, feature_layer_final])
b_fc2_m = bias_variable([feature_layer_final])

y_conv_m = tf.nn.softmax(tf.matmul(h_fc1_m, W_fc2_m) + b_fc2_m)

sess_m.run(tf.global_variables_initializer())


def init_move_selector():
    # create model saver
    saver = tf.train.Saver()
    with sess_m.as_default():
        saver.restore(sess_m, '../model/my-model-' + piece_type)

def close_move_selector():
    sess_m.close()

def move_selector_nn(fen, move):
    output, piece_type = extract_features_dest(fen, move)
    print piece_type
    feature = np.zeros((1, 810))
    feature[0] = output[0:-1].split(',')
    
    prediction = y_conv_m.eval(feed_dict={x_m: feature})
    prediction = np.reshape(prediction, (10, 9)).astype(np.float32)
    
    return prediction