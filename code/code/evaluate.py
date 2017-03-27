# -------------------------------------------------------------+
# Ver 1.0    Mar 13 2017                                       |
# Author: zhz                                                  |
# Summary: use the model to calculate the score of current     |
#          status                                              |
# -------------------------------------------------------------+


import tensorflow as tf
import numpy as np
import os
import information_eva as ie
import copy as cp

def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def evaluate(fen):
    feature_chnl = 10

    feature_layer_1 = 64
    feature_layer_2 = 128

    feature_layer_soft = 256
    feature_layer_final = 1

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

    # output layer
    W_fc2 = weight_varible([feature_layer_soft, feature_layer_final])
    b_fc2 = bias_variable([feature_layer_final])

    y_conv = tf.matmul(h_fc1, W_fc2) + b_fc2
    y_ = tf.placeholder(tf.float32, [None, feature_layer_final])

    # model training
    cost = tf.reduce_mean(tf.square(y_conv-y_))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cost)

    sess.run(tf.global_variables_initializer())

    # create model saver
    saver = tf.train.Saver()

    path = '../eva_train/'
    model_path = '../eva_model/'

    print fen
    data = ie.extract_features_eva(fen)
    feature = np.zeros((1,900))
#    print feature
    feature[0] = (data[0:-1].split(','))[0:900]
    with sess.as_default():
        saver.restore(sess,model_path + 'my-model-1450000')
        prediction=y_conv.eval(feed_dict={x: feature})
    sess.close()
    return prediction

# print evaluate("r1bakabnr/111111111/1c11111c1/p1p111p1p/111111111/111111111/P1P111P1P/1C11111C1/111111111/R1BAKABNR/b")
# print evaluate("rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/b")
# print evaluate("rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r")
#     # should be open the real-time game results file with rewards
# print evaluate("r11akabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABN1/b")
#print evaluate("r11akabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABN1/r")

import ctypes
import check as ck
evaluator = ctypes.CDLL('/root/code/example.so')


def eval_move(board, move,size,side):
    score = np.zeros(size)
    print move
    for x in xrange(0,size):
        newboard = cp.deepcopy(board)
        string = move[x]
        newboard[int(string[2])][int(string[3])]=newboard[int(string[0])][int(string[1])]
        newboard[int(string[0])][int(string[1])]='1';


        fen=""
        for i in xrange(0,10):
            for j in xrange(0,9):
                fen += newboard[i][j]
            fen += "/"
        # fen += side
        if side=='r':
            fen += "b"
        else:
            fen += 'r'
            pass

        print fen
        isChecked, _ = ck.check(newboard,side)
        if isChecked == 1:
            score[x] = 9999
            continue
        # evaluator.evaluate.argtypes = [ctypes.c_char_p]
        score[x]=evaluator.evaluate(fen)
        # score[x] = evaluate(fen)


    index = np.argmin(score)
    print score
    print index
    return index

    pass

