import random
import copy
import tensorflow as tf
import os
import numpy as np
from socketIO_client import SocketIO
import time
from piece_selector import *
from move_selector import *
from check import *
from evaluate import *

piece_b = ['k', 'a', 'b', 'n', 'r', 'c', 'p']
piece_r = ['K', 'A', 'B', 'N', 'R', 'C', 'P']
piece_list = {'b': piece_b, 'r': piece_r}
piece_list_op = {'b': piece_r, 'r': piece_b}


precision = 18
move = np.zeros((precision, 4), dtype=np.int)

# load NN models
fuck = Fuck()
fuck.init_piece_selector()
fuck_a = Fuck_m("a")
fuck_a.init_move_selector()
fuck_b = Fuck_m("b")
fuck_b.init_move_selector()
fuck_c = Fuck_m("c")
fuck_c.init_move_selector()
fuck_k = Fuck_m("k")
fuck_k.init_move_selector()
fuck_p = Fuck_m("p")
fuck_p.init_move_selector()
fuck_r = Fuck_m("r")
fuck_r.init_move_selector()
fuck_n = Fuck_m("n")
fuck_n.init_move_selector()


# get max value index from prediction
def get_max(prediction):
    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i, j

# process piece selector prediction
def process_piece(prediction, fen, player):
    for i in range(10):
        for j in range(9):
            temp_r, temp_c = flip(fen, i, j)    
            if (fen[i*10+j] == '1'):
                prediction[temp_r][temp_c]=0.0
            elif (fen[i*10+j] in piece_list_op[player]):
                prediction[temp_r][temp_c]=0.0

    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total

    
# process move selector prediction
def process_move(prediction):
    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total


def random_select(prediction):
    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total

    rand = np.random.uniform(0,1)
    temp = 0
    for i in range(10):
        for j in range(9):
            temp += prediction[i][j]
            if (temp > rand):
                return i,j


def printstat(prediction):
    temp = np.zeros((10,9))
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    for i in range(10):
        for j in range(9):
            temp[i][j] = prediction[9-i][8-j]
            print temp[i]


def flip(fen, x, y):
    if fen[100] =='b':
        x = 9 - x
        y = 8 - y
    return x, y


def move_selection(fen,newboard):
    prediction = fuck.piece_selector_nn(fen)
    process_piece(prediction,fen,fen[100])
    for i in range(precision):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break
        temp1 = move[i][0]
        temp2 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])

        # move selector
        output, piece_type = extract_features_dest(fen, [move[i][0], move[i][1]])
        if piece_type == "a":
            prediction_m = fuck_a.move_selector_nn(output)
        elif piece_type == "b":
            prediction_m = fuck_b.move_selector_nn(output)
        elif piece_type == "c":
            prediction_m = fuck_c.move_selector_nn(output)
        elif piece_type == "n":
            prediction_m = fuck_n.move_selector_nn(output)
        elif piece_type == "k":
            prediction_m = fuck_k.move_selector_nn(output)
        elif piece_type == "p":
            prediction_m = fuck_p.move_selector_nn(output)
        elif piece_type == "r":
            prediction_m = fuck_r.move_selector_nn(output)
        pass
        # process prediction
        move[i][2], move[i][3] = get_max(prediction_m)
        move[i][2], move[i][3] = flip(fen, move[i][2], move[i][3])

        prediction[temp1][temp2] = 0.0


    index = eval_move(newboard,move[:i],i,fen[100])

    return index
