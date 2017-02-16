import tensorflow as tf
import os
import numpy as np


def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# read input
# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# print("Download Done!")
feature_chnl = 8

feature_layer_1 = 32
feature_layer_2 = 128

feature_layer_soft = 256
feature_layer_final = 90

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
y_ = tf.placeholder(tf.float32, [None, feature_layer_final])

# model training
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-3).minimize(cross_entropy)

correct_prediction = tf.equal(tf.arg_max(y_conv, 1), tf.arg_max(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())

# create model saver
saver = tf.train.Saver()

path = '../train_shuffle/'
for filename in os.listdir(path):
    if filename[0] == '.':
        continue
    pgn = open(path + filename, 'r')
    batch = 1000
    feature = np.zeros((batch/2, 720))
    result = np.zeros((batch/2, 90))
    count = 0
    for line in pgn:
        if count%2 == 0:
            feature[(count%batch)/2] = line[0:-2].split(',')
        else:
            result[(count%batch)/2] = line[0:-2].split(',')
        if count % 10000 == 9999:
            saver.save(sess, 'my-model', global_step = (count+1)/2)
            train_accuacy = accuracy.eval(feed_dict={x: feature, y_: result})
            print("step %d, training accuracy %g"%((count+1)/2, train_accuacy))
        if count != 0 and count%batch == batch - 1:
            train_step.run(feed_dict = {x: feature, y_: result})
        count += 1
        

# # accuacy on test
# print("test accuracy %g"%(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})))