# -------------------------------------------------------------+
# Ver 1.0    Mar 13 2017                                       |
# Author: zxm                                                  |
# Summary: to train a evaluation model by supervised learning  |
#          using processed source data                         |
# -------------------------------------------------------------+


import tensorflow as tf
import numpy as np
import os


def weight_varible(shape, name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name=name)


def bias_variable(shape, name):
    initial = tf.zeros(shape=shape)
    return tf.Variable(initial, name=name)


def train_eva_model():
    # NN config
    input_layer = 200
    hidden_layer_1 = 64
    hidden_layer_2 = 128
    hidden_layer_3 = 512
    output_layer = 1

    tf.reset_default_graph()
    sess = tf.InteractiveSession()

    # input
    x = tf.placeholder(tf.float32, [None, input_layer])

    # full layer-1
    W_full1 = weight_varible([input_layer, hidden_layer_1], 'W_full1')
    b_full1 = bias_variable([hidden_layer_1], 'b_full1')
    h_full1 = tf.nn.relu(tf.matmul(x, W_full1) + b_full1)

    # full layer-2
    W_full2 = weight_varible([hidden_layer_1, hidden_layer_2], 'W_full2')
    b_full2 = bias_variable([hidden_layer_2], 'b_full2')
    h_full2 = tf.nn.relu(tf.matmul(h_full1, W_full2) + b_full2)

    # full layer-3
    W_full3 = weight_varible([hidden_layer_2, hidden_layer_3], 'W_full3')
    b_full3 = bias_variable([hidden_layer_3], 'b_full3')
    h_full3 = tf.nn.relu(tf.matmul(h_full2, W_full3) + b_full3)

    # output layer
    W_out = weight_varible([hidden_layer_3, output_layer])
    b_out = bias_variable([output_layer])
    y_out = tf.matmul(h_full3, W_out) + b_out

    # target output
    y_ = tf.placeholder(tf.float32, [None, output_layer])

    # model training
    cost = tf.reduce_mean(tf.square(y_out-y_))
    train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(cost)

    sess.run(tf.global_variables_initializer())

    # create model saver
    saver = tf.train.Saver()

    path = '../eva_train/'
    model_path = '../eva_model/'

    for filename in os.listdir(path):
        if filename[0] == '.':
            continue
        pgn = open(path + filename, 'r')

        batch = 1000
        x_in = np.zeros((batch/2, 900))
        y_eva = np.zeros((batch/2, 1))
        count = 0
        for line in pgn:
            if count%3 == 0:
                x_in[(count%batch)/2] = line[0:-2].split(',')
            elif count%3 == 1:
                y_eva[(count%batch)/2] = int(line)

            if count % 10000 == 9999:
                saver.save(sess, model_path + 'eva-model', global_step = (count+1)/2)
                train_cost = cost.eval(feed_dict={x: x_in, y_: y_eva})
                print("step %d, training cost %g"%((count+1)/2, train_cost))

            if count != 0 and count%batch == batch - 1:
                train_step.run(feed_dict = {x: x_in, y_: y_eva})
                x_in = np.zeros((batch/2, 900))
                y_eva = np.zeros((batch/2, 1))

            count += 1

    if count != 0 and count%batch != batch - 1:
        train_step.run(feed_dict = {x: x_in[:(count%batch)/2,:], y_: y_eva[:(count%batch)/2,:]})
    saver.save(sess, model_path + 'eva-model', global_step = (count+1)/2)
    print count

train_eva_model()
