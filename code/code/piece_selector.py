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


def piece_selector_nn(fen):
    feature_chnl = 8

    feature_layer_1 = 32
    feature_layer_2 = 128

    feature_layer_soft = 256
    feature_layer_final = 90

    tf.reset_default_graph()
    sess = tf.InteractiveSession()

    # paras
    # 32? to be determined
    W_conv1 = weight_varible([3, 3, feature_chnl, feature_layer_1])
    b_conv1 = bias_variable([feature_layer_1])

    # conv layer-1
    x = tf.placeholder(tf.float32, [None, 9*10*feature_chnl])
    x_image = tf.reshape(x, [-1, 10, 9, feature_chnl])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    # conv layer-2
    W_conv2 = weight_varible([3, 3, feature_layer_1, feature_layer_2])
    b_conv2 = bias_variable([feature_layer_2])

    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)

    # full connection
    W_fc1 = weight_varible([10 * 9 * feature_layer_2, feature_layer_soft])
    b_fc1 = bias_variable([feature_layer_soft])

    h_conv2_flat = tf.reshape(h_conv2, [-1, 10 * 9 * feature_layer_2])
    h_fc1 = tf.nn.relu(tf.matmul(h_conv2_flat, W_fc1) + b_fc1)

    # output layer: softmax
    W_fc2 = weight_varible([feature_layer_soft, feature_layer_final])
    b_fc2 = bias_variable([feature_layer_final])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

    sess.run(tf.global_variables_initializer())

    # create model saver
    saver = tf.train.Saver()

    output = extract_features_piece(fen)
    feature = np.zeros((1, 720))
    feature[0] = output[0:-1].split(',')
    with sess.as_default():
        saver.restore(sess, '../model/my-model-piece_selector')
        prediction = y_conv.eval(feed_dict={x: feature})
        prediction = np.reshape(prediction, (10, 9)).astype(np.float32)
    sess.close()
    return prediction