# -------------------------------------------------------------+
# Ver 1.0    Mar 13 2017                                       |
# Author: zxm                                                  |
# Summary: to train a evaluation model by supervised learning  |
#          using processed source data                         |
# -------------------------------------------------------------+


import tensorflow as tf
import numpy as np
import os
import information_eva

def weight_varible(shape, name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name=name)


def bias_variable(shape, name):
    initial = tf.zeros(shape=shape)
    return tf.Variable(initial, name=name)

class Eval_model(object):
    def __init__(self):
        input_layer = 123
        hidden_layer_1 = 256
        hidden_layer_2 = 512
        hidden_layer_3 = 256
        output_layer = 1

        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()

        # input
        self.x = tf.placeholder(tf.float32, [None, input_layer])

        # full layer-1
        self.W_full1 = weight_varible([input_layer, hidden_layer_1], 'W_full1')
        self.b_full1 = bias_variable([hidden_layer_1], 'b_full1')
        self.h_full1 = tf.nn.relu(tf.matmul(self.x, self.W_full1) + self.b_full1)

        # full layer-2
        self.W_full2 = weight_varible([hidden_layer_1, hidden_layer_2], 'W_full2')
        self.b_full2 = bias_variable([hidden_layer_2], 'b_full2')
        self.h_full2 = tf.nn.relu(tf.matmul(self.h_full1, self.W_full2) + self.b_full2)

        # full layer-3
        self.W_full3 = weight_varible([hidden_layer_2, hidden_layer_3], 'W_full3')
        self.b_full3 = bias_variable([hidden_layer_3], 'b_full3')
        self.h_full3 = tf.nn.relu(tf.matmul(self.h_full2, self.W_full3) + self.b_full3)

        # output layer
        self.W_out = weight_varible([hidden_layer_3, output_layer],'W_out')
        self.b_out = bias_variable([output_layer],'b_out')
        self.y_out = tf.matmul(self.h_full3, self.W_out) + self.b_out

        # target output
        # self.y_ = tf.placeholder(tf.float32, [None, output_layer])
        pass

    def init_evaluator(self):
        # self.sess.run(tf.global_variables_initializer())
        print self.sess
        with self.sess.as_default():       
            saver = tf.train.Saver()
            saver.restore(self.sess, '../eva_model/eva-model-968675')

    def close_evaluator(self):
        self.sess.close()

    def evaluate(self,fen):
        output = information_eva.ext_info_eva_full(fen + ",0")
        output = output.split("\n")[0]
        x_in = np.zeros((1, 123))
        x_in[0] = output[0:-2].split(',')
        with self.sess.as_default():
            prediction = self.y_out.eval(feed_dict={self.x: x_in})

        return prediction
    
def train_eva_model():
    # NN config
    input_layer = 123
    hidden_layer_1 = 256
    hidden_layer_2 = 512
    hidden_layer_3 = 256
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
    W_out = weight_varible([hidden_layer_3, output_layer],'W_out')
    b_out = bias_variable([output_layer],'b_out')
    y_out = tf.matmul(h_full3, W_out) + b_out

    # target output
    y_ = tf.placeholder(tf.float32, [None, output_layer])

    # model training
    cost = tf.reduce_mean(tf.abs(y_out-y_))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cost)

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
        x_in = np.zeros((batch/2, 123))
        y_eva = np.zeros((batch/2, 1))
        count = 0
        for line in pgn:
            if len(line) < 2:
                continue
                
            if count % 2 == 0:
                x_in[(count % batch) / 2] = line[0:-2].split(',')
            elif count % 2 == 1:
                score =int(line)
                if (score > 0):
                    if (score <= 100):
                        score = score / 10
                    elif (score >= 9000):
                        score = 20
                    else:
                        score = 10 + np.sqrt((score - 100) / 6)
                elif (score < 0):
                    if (score >= -100):
                        score = score / 10
                    elif (score <= 9000):
                        score = -20
                    else:
                        score = -10 - np.sqrt((-1 * score - 100) / 6)

                y_eva[(count%batch)/2] = score

            if count % 10000 == 9999:
                saver.save(sess, model_path + 'eva-model', global_step = (count+1)/2)
                train_cost = cost.eval(feed_dict={x: x_in, y_: y_eva})
                print("step %d, training cost %g"%((count+1)/2, train_cost))

            if count != 0 and count%batch == batch - 1:
                train_step.run(feed_dict = {x: x_in, y_: y_eva})
                x_in = np.zeros((batch/2, 123))
                y_eva = np.zeros((batch/2, 1))

            count += 1

    if count != 0 and count%batch != batch - 1:
        train_step.run(feed_dict = {x: x_in[:(count%batch)/2,:], y_: y_eva[:(count%batch)/2,:]})
    saver.save(sess, model_path + 'eva-model', global_step = (count+1)/2)
    print count

if __name__ == '__main__': 
    train_eva_model()
